from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import routeros_api
import socket
from fastapi.middleware.cors import CORSMiddleware
import logging




app = FastAPI()

# --- CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Router Config Storage ---
router_config = {}

# --- Request Models ---
class RouterCredentials(BaseModel):
    host: str
    username: str
    password: str
    port: Optional[int] = 8728

class ServiceConfigRequest(BaseModel):
    service_types: List[str]
    ether_ports: List[str]
    enable_antisharing: Optional[bool] = False


# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- Router Connection ---
def connect_to_router():
    try:
        if not router_config:
            raise HTTPException(status_code=400, detail="Router credentials not set")

        connection = routeros_api.RouterOsApiPool(
            host=router_config["host"],
            username=router_config["username"],
            password=router_config["password"],
            port=router_config.get("port", 8728),
            plaintext_login=True
        )
        logger.info("Connected to MikroTik router.")
        return connection.get_api()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Router connection failed: {str(e)}")

# --- Utility: Logger ---
def log(message: str, logs: List[str]):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    logs.append(f"{timestamp} {message}")

# --- Endpoint: Set Router Credentials ---
@app.post("/set-router")
def set_router_creds(creds: RouterCredentials):
    router_config.update(creds.dict())
    return {"message": "Router credentials saved"}

# --- Endpoint: Ping Router ---
@app.get("/ping-router")
def ping_router():
    try:
        host = router_config.get("host")
        if not host:
            raise HTTPException(status_code=400, detail="Router IP not set")
        socket.setdefaulttimeout(2)
        socket.socket().connect((host, 8728))
        return {"online": True}
    except Exception:
        return {"online": False}

# --- Endpoint: Scan Router Capabilities ---
@app.get("/scan-router")
def scan_router():
    try:
        api = connect_to_router()
        interfaces = api.get_resource('/interface').get()
        has_hotspot = bool(api.get_resource('/ip/hotspot').get())
        has_pppoe = bool(api.get_resource('/interface/pppoe-server/server').get())

        ports = [iface['name'] for iface in interfaces if iface['type'] in ["ether", "wlan"]]
        return {
            "interfaces": ports,
            "hotspot_configured": has_hotspot,
            "pppoe_configured": has_pppoe
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- API Endpoint ---
@app.post("/configure-services")
def configure_services(request: ServiceConfigRequest):
    logs = []
    try:
        api = connect_to_router()
        log("Initiating configuration...", logs)

        # Create bridge
        log("Setting up network bridge...", logs)
        bridge_res = api.get_resource('/interface/bridge')
        bridge_res.add(name="bridge")
        log("Creating bridge interface...", logs)

        # Add ports to bridge
        log("Adding selected ports to bridge...", logs)
        ports_res = api.get_resource('/interface/bridge/port')
        for port in request.ether_ports:
            ports_res.add(interface=port, bridge="bridge")

        # Configure IP (assuming DHCP server range)
        log("Configuring IP addressing...", logs)
        ip_address = api.get_resource('/ip/address')
        ip_address.add(address="192.168.88.1/24", interface="bridge")

        # Configure DHCP Server
        log("Setting up DHCP server...", logs)
        pool_res = api.get_resource('/ip/pool')
        pool_res.add(name="dhcp-pool", ranges="192.168.88.10-192.168.88.254")

        dhcp_res = api.get_resource('/ip/dhcp-server')
        dhcp_res.add(name="dhcp1", interface="bridge", address_pool="dhcp-pool")

        dhcp_net = api.get_resource('/ip/dhcp-server/network')
        dhcp_net.add(
            address="192.168.88.0/24",
            gateway="192.168.88.1",
            dns_server="8.8.8.8"
        )

        # Hotspot Configuration
        if "hotspot" in request.service_types:
            log("Configuring Hotspot service...", logs)

            hs_profile = api.get_resource('/ip/hotspot/profile')
            hs_profile.add(
                name="hs-profile",
                hotspot_address="192.168.88.1",
                use_radius="yes",
                login_by="http-pap"
            )

            hs_setup = api.get_resource('/ip/hotspot')
            hs_setup.add(name="hs1", interface="bridge", address_pool="dhcp-pool", profile="hs-profile")

            # Walled Garden Rule
            walled_garden = api.get_resource('/ip/hotspot/walled-garden')
            walled_garden.add(
                dst_host="library-yihr.vercel.app",
                action="accept"
            )

            # Anti-Sharing Protection (TTL mangle)
            if request.enable_antisharing:
                log("Enabling Hotspot Anti-Sharing Protection...", logs)
                mangle = api.get_resource('/ip/firewall/mangle')
                mangle.add(
                    chain="postrouting",
                    action="change-ttl",
                    new_ttl="set:1",
                    passthrough="yes"
                )

        # PPPoE Server Configuration
        if "pppoe" in request.service_types:
            log("Configuring PPPoE service...", logs)
            ppp_prof = api.get_resource('/ppp/profile')
            ppp_prof.add(name="pppoe-prof", use_radius="yes")

            pppoe_server = api.get_resource('/interface/pppoe-server/server')
            pppoe_server.add(service_name="pppoe-service", interface="bridge", profile="pppoe-prof")

        log("Configuration complete!", logs)
        return {"status": "success", "logs": logs}

    except Exception as e:
        log(f"❌ Error: {str(e)}", logs)
        return {"status": "error", "logs": logs}