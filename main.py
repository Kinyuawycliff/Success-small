# from fastapi import FastAPI, HTTPException, Depends

# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import routeros_api


# from sqlalchemy.exc import OperationalError
# from pydantic import BaseModel, root_validator
# from typing import Optional, Literal
# from sqlalchemy import create_engine, text, Column, Integer, String, Float
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from sqlalchemy.exc import SQLAlchemyError

# from pydantic import BaseModel, ValidationError, model_validator
# from typing import Optional, Literal, List
# from datetime import date
# import paramiko






# # --- FastAPI app ---
# app = FastAPI()

# # --- CORS ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Use specific domain in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- PostgreSQL Database Setup ---
# DATABASE_URL = "postgresql://MikrotikDB_owner:npg_56LBlfUTePyM@ep-wispy-scene-a8v3hj9a-pooler.eastus2.azure.neon.tech/MikrotikDB?sslmode=require"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Create DB tables (run once or manage migrations separately)
# Base.metadata.create_all(bind=engine)



# # --- Database Model ---
# class Package(Base):
#     __tablename__ = "packages"

#     id = Column(Integer, primary_key=True, index=True)
#     package_type = Column(String, nullable=False)   # hotspot, pppoe, dataplan, freetrial
#     name = Column(String, nullable=False)           # e.g. "10mbps unlimited"
#     session_time = Column(String, nullable=False)   # e.g. "1h30m"
#     bandwidth = Column(String, nullable=False)      # e.g. "2M/2M"
#     devices = Column(Integer, nullable=False)
#     price = Column(Float, nullable=False)            # mandatory for all packages
#     data = Column(String, nullable=True)             # mandatory only for dataplan


# # --- Pydantic Schema ---
# class PackageCreate(BaseModel):
#     package_type: Literal["hotspot", "pppoe", "dataplan", "freetrial"]
#     name: str
#     session_time: str
#     upload_speed: str
#     download_speed: str
#     devices: int
#     price: int
#     data: Optional[str] = None

#     @model_validator(mode="after")
#     def check_data_for_dataplan(cls, values):
#         if values.package_type == "dataplan" and not values.data:
#             raise ValueError("Data is required for dataplan package type")
#         return values
    



# class PackageUpdate(BaseModel):
#     package_type: str
#     name: str
#     session_time: str
#     upload_speed: str
#     download_speed: str
#     devices: int
#     price: float
#     data: str




# class PackageResponse(BaseModel):
#     id: int
#     package_type: str
#     name: str
#     session_time: str
#     bandwidth: str
#     devices: int
#     price: float
#     data: Optional[str]

#     class Config:
#         from_attributes = True



# #  --- ISP PPPoE & Hotspot DATABASE MODELS ---

# # SQLALCHEMY DATABASE CONNECTION
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, nullable=False)
#     phone = Column(String, nullable=False)
#     user_type = Column(String, nullable=False)  # "Hotspot" or "PPPoE"
#     package = Column(String, nullable=True)
#     expiry = Column(String, default="Expired")
#     last_online = Column(String, default="Never")
#     password = Column(String, nullable=False)



# # Pydantic Schemas for User

# class UserCreate(BaseModel):
#     username: str
#     phone: str
#     user_type: Literal["Hotspot", "PPPoE"]
#     package: Optional[str] = None
#     expiry: Optional[str] = "Expired"
#     last_online: Optional[str] = "Never"
#     password: str


# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     phone: Optional[str] = None
#     user_type: Optional[Literal["Hotspot", "PPPoE"]] = None
#     package: Optional[str] = None
#     expiry: Optional[str] = None
#     last_online: Optional[str] = None
#     password: Optional[str] = None


# class UserResponse(BaseModel):
#     id: int
#     username: str
#     phone: str
#     user_type: str
#     package: Optional[str]
#     expiry: Optional[date] 
#     last_online: Optional[str]
#     password: str

# class Config:
#     from_attributes = True



# # --- MikroTik Device Model ---
# class MikroTikDevice(Base):
#     __tablename__ = "mikrotik_devices"

#     id = Column(Integer, primary_key=True, index=True)
#     ip_address = Column(String, nullable=False)
#     username = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     api_port = Column(Integer, default=8728)
#     # method = Column(String, nullable=False)  # api or ssh




# #! --- MikroTik Device Schemas ---
# # class MikroTikDeviceCreate(BaseModel):
# #     host: str
# #     username: str
# #     password: str
# #     port: Optional[int] = 8728
# #     method: Literal["api", "ssh"]

# class MikroTikDeviceCreate(BaseModel):
#     ip_address: str
#     username: str
#     password: str
#     api_port: int = 8728  # default API port


# class MikroTikDeviceResponse(BaseModel):
#     id: int
#     device_name: str
#     ip_address: str
#     username: str
#     password: str
#     connection_method: str
#     api_port: Optional[int]
#     ssh_port: Optional[int]
#     web_port: Optional[int]
#     web_enabled: Optional[bool]
#     winbox_enabled: Optional[bool]
#     ssh_enabled: Optional[bool]
#     status: Optional[str]

#     class Config:
#         orm_mode = True




# # --- Dependency ---
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



# # --- Log DB connection on startup ---
# @app.on_event("startup")
# def startup_event():
#     try:
#         with engine.connect() as connection:
#             connection.execute(text("SELECT 1"))  # <- Use text() here
#         print("✅ Successfully connected to the PostgreSQL database.")
#     except OperationalError as e:
#         print("❌ Failed to connect to the PostgreSQL database.")
#         print(str(e))


# # --- MikroTik Connection Helper ---
# # def connect_to_router():
# #     connection = routeros_api.RouterOsApiPool(
# #         host='192.168.100.2',
# #         username='admin',
# #         password='123456',
# #         port=8728,
# #         plaintext_login=True
# #     )
# #     return connection.get_api()


# def connect_to_router():
#     db = SessionLocal()
#     device = db.query(MikroTikDevice).first()
#     db.close()

#     if not device:
#         raise Exception("No MikroTik device found in the database.")

#     connection = routeros_api.RouterOsApiPool(
#         host=device.ip_address,
#         username=device.username,
#         password=device.password,
#         port=device.api_port,
#         plaintext_login=True
#     )
#     return connection.get_api()



# # --- Home Route ---
# @app.get("/")
# def home():
#     return {"message": "MikroTik Billing API is running"}

# # --- Active Hotspot Users ---
# @app.get("/active-users")
# def get_active_users():
#     api = connect_to_router()
#     users = api.get_resource('/ip/hotspot/active').get()
#     return users

# # --- Disconnect Hotspot User ---
# class IPRequest(BaseModel):
#     ip_address: str

# @app.post("/disconnect-user")
# def disconnect_user(request: IPRequest):
#     api = connect_to_router()
#     active = api.get_resource('/ip/hotspot/active')
#     users = active.get()

#     target_user = next((user for user in users if user.get("address") == request.ip_address), None)

#     if not target_user:
#         raise HTTPException(status_code=404, detail="IP address not found in active sessions")

#     print("TARGET USER DATA:", target_user)
#     print("Keys:", target_user.keys())

#     active.remove(id=target_user['id'])  # Adjust if needed

#     return {"message": f"User with IP {request.ip_address} has been disconnected"}





# # --- Packages Endpoints ---

# @app.get("/packages", response_model=List[PackageResponse])
# def get_packages(db: Session = Depends(get_db)):
#     try:
#         packages = db.query(Package).all()
#         return packages
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




# @app.post("/create-package")
# def create_package(package: PackageCreate, db: Session = Depends(get_db)):
#     bandwidth = f"{package.upload_speed}/{package.download_speed}"

#     new_package = Package(
#         package_type=package.package_type,
#         name=package.name,
#         session_time=package.session_time,
#         bandwidth=bandwidth,
#         devices=package.devices,
#         price=package.price,
#         data=package.data,
#     )

#     try:
#         db.add(new_package)
#         db.commit()
#         db.refresh(new_package)
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Database error: " + str(e))

#     return {
#         "message": "Package created successfully",
#         "package": {
#             "id": new_package.id,
#             "name": new_package.name,
#             "bandwidth": new_package.bandwidth,
#             "price": new_package.price,
#             "data": new_package.data,
#         },
#     }



# @app.delete("/packages/{package_id}", status_code=204)
# def delete_package(package_id: int, db: Session = Depends(get_db)):
#     package = db.query(Package).filter(Package.id == package_id).first()
#     if not package:
#         raise HTTPException(status_code=404, detail="Package not found")
    
#     db.delete(package)
#     db.commit()
#     return {"message": "Package deleted successfully"}





# @app.put("/packages/{package_id}")
# def update_package(package_id: int, updated_package: PackageUpdate, db: Session = Depends(get_db)):
#     package = db.query(Package).filter(Package.id == package_id).first()

#     if not package:
#         raise HTTPException(status_code=404, detail="Package not found")

#     package.package_type = updated_package.package_type
#     package.name = updated_package.name
#     package.session_time = updated_package.session_time
#     package.bandwidth = f"{updated_package.upload_speed}/{updated_package.download_speed}"  # ✅ fixed here
#     package.devices = updated_package.devices
#     package.price = updated_package.price
#     package.data = updated_package.data

#     db.commit()
#     db.refresh(package)

#     return package





# # Users Endpoints

# @app.get("/users", response_model=List[UserResponse])
# def get_users(db: Session = Depends(get_db)):
#     try:
#         users = db.query(User).all()
#         return users
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# @app.post("/create-user", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     new_user = User(**user.dict())
#     try:
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Database error: " + str(e))



# @app.put("/users/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     for key, value in user_update.dict(exclude_unset=True).items():
#         setattr(user, key, value)

#     db.commit()
#     db.refresh(user)
#     return user


# @app.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(user)
#     db.commit()
#     return {"message": f"User with ID {user_id} deleted successfully"}






# # --- Test MikroTik API Connection ---
# @app.post("/test-mikrotik-connection")
# def test_mikrotik_connection(device: MikroTikDeviceCreate,  db: Session = Depends(get_db)):
#     try:
#         connection = routeros_api.RouterOsApiPool(
#             host=device.host,
#             username=device.username,
#             password=device.password,
#             port=device.port,
#             plaintext_login=True
#         )
#         api = connection.get_api()
        
#         # Try to fetch system resource to confirm connection
#         api.get_resource('/system/resource').get()

#         # Print success message to console
#         print(f"[✅] Successfully connected to MikroTik router at {device.host}")

#         # Always close the connection
#         connection.disconnect()
        


#         # Check if device already exists
#         # existing = db.query(MikroTikDevice).filter_by(host=device.host).first()
#         # if existing:
#         #     existing.username = device.username
#         #     existing.password = device.password
#         #     existing.port = device.port
#         # else:
#         #     new_device = MikroTikDevice(
#         #         host=device.host,
#         #         username=device.username,
#         #         password=device.password,
#         #         port=device.port
#         #     )
#         #     db.add(new_device)

#         # db.commit()
#         # return {"message": "Successfully connected and saved MikroTik device", "device": device.host}






#         return {"message": "Successfully connected to MikroTik router via API"}
#     except Exception as e:
#         print(f"[❌] Connection to MikroTik router at {device.host} failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")


# # --- Test MikroTik SSH Connection ---

# @app.post("/test-mikrotik-ssh-connection")
# def test_ssh_connection(device: MikroTikDeviceCreate):
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(
#             hostname=device.host,
#             port=device.port,
#             username=device.username,
#             password=device.password,
#             timeout=10
#         )
#         ssh.close()
#         return {"message": "Successfully connected via SSH"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"SSH connection failed: {str(e)}")



# # --- Link MikroTik Device ---
# @app.post("/link-mikrotik", response_model=MikroTikDeviceResponse)
# def link_device(device: MikroTikDeviceCreate, db: Session = Depends(get_db)):
#     new_device = MikroTikDevice(**device.dict())
#     try:
#         db.add(new_device)
#         db.commit()
#         db.refresh(new_device)
#         return new_device
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
    


# @app.get("/mikrotiks", response_model=List[MikroTikDeviceResponse])
# def get_devices(db: Session = Depends(get_db)):
#     try:
#         return db.query(MikroTikDevice).all()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # --- Delete MikroTik Device ---
# @app.delete("/mikrotiks/{device_id}")
# def delete_device(device_id: int, db: Session = Depends(get_db)):
#     device = db.query(MikroTikDevice).filter(MikroTikDevice.id == device_id).first()
#     if not device:
#         raise HTTPException(status_code=404, detail="Device not found")
#     try:
#         db.delete(device)
#         db.commit()
#         return {"message": "Device deleted successfully"}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))











































# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, model_validator
# from typing import Optional, Literal, List
# from datetime import date
# import routeros_api
# import paramiko

# from sqlalchemy import create_engine, text, Column, Integer, String, Float
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from sqlalchemy.exc import SQLAlchemyError, OperationalError

# # --- FastAPI app ---
# app = FastAPI(title="MikroTik Billing API", version="1.0.0")

# # --- CORS ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Use specific domains in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- PostgreSQL Database Setup ---
# DATABASE_URL = "postgresql://MikrotikDB_owner:npg_56LBlfUTePyM@ep-wispy-scene-a8v3hj9a-pooler.eastus2.azure.neon.tech/MikrotikDB?sslmode=require"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # --- Database Models ---
# class Package(Base):
#     __tablename__ = "packages"

#     id = Column(Integer, primary_key=True, index=True)
#     package_type = Column(String, nullable=False)   # hotspot, pppoe, dataplan, freetrial
#     name = Column(String, nullable=False)           # e.g. "10mbps unlimited"
#     session_time = Column(String, nullable=False)   # e.g. "1h30m"
#     bandwidth = Column(String, nullable=False)      # e.g. "2M/2M"
#     devices = Column(Integer, nullable=False)
#     price = Column(Float, nullable=False)
#     data = Column(String, nullable=True)            # mandatory only for dataplan

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, nullable=False, unique=True)
#     phone = Column(String, nullable=False)
#     user_type = Column(String, nullable=False)      # "Hotspot" or "PPPoE"
#     package = Column(String, nullable=True)
#     expiry = Column(String, default="Expired")
#     last_online = Column(String, default="Never")
#     password = Column(String, nullable=False)

# class MikroTikDevice(Base):
#     __tablename__ = "mikrotik_devices"

#     id = Column(Integer, primary_key=True, index=True)
#     ip_address = Column(String, nullable=False, unique=True)
#     username = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     api_port = Column(Integer, default=8728)

# # Create DB tables
# Base.metadata.create_all(bind=engine)

# # --- Pydantic Schemas ---
# class PackageCreate(BaseModel):
#     package_type: Literal["hotspot", "pppoe", "dataplan", "freetrial"]
#     name: str
#     session_time: str
#     upload_speed: str
#     download_speed: str
#     devices: int
#     price: float
#     data: Optional[str] = None

#     @model_validator(mode="after")
#     def check_data_for_dataplan(self):
#         if self.package_type == "dataplan" and not self.data:
#             raise ValueError("Data is required for dataplan package type")
#         return self

# class PackageUpdate(BaseModel):
#     package_type: Optional[Literal["hotspot", "pppoe", "dataplan", "freetrial"]] = None
#     name: Optional[str] = None
#     session_time: Optional[str] = None
#     upload_speed: Optional[str] = None
#     download_speed: Optional[str] = None
#     devices: Optional[int] = None
#     price: Optional[float] = None
#     data: Optional[str] = None

# class PackageResponse(BaseModel):
#     id: int
#     package_type: str
#     name: str
#     session_time: str
#     bandwidth: str
#     devices: int
#     price: float
#     data: Optional[str] = None

#     class Config:
#         from_attributes = True

# class UserCreate(BaseModel):
#     username: str
#     phone: str
#     user_type: Literal["Hotspot", "PPPoE"]
#     package: Optional[str] = None
#     expiry: Optional[str] = "Expired"
#     last_online: Optional[str] = "Never"
#     password: str

# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     phone: Optional[str] = None
#     user_type: Optional[Literal["Hotspot", "PPPoE"]] = None
#     package: Optional[str] = None
#     expiry: Optional[str] = None
#     last_online: Optional[str] = None
#     password: Optional[str] = None

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     phone: str
#     user_type: str
#     package: Optional[str] = None
#     expiry: str
#     last_online: str
#     password: str

#     class Config:
#         from_attributes = True

# class MikroTikDeviceCreate(BaseModel):
#     ip_address: str
#     username: str
#     password: str
#     api_port: int = 8728

# class MikroTikDeviceResponse(BaseModel):
#     id: int
#     ip_address: str
#     username: str
#     password: str
#     api_port: int

#     class Config:
#         from_attributes = True

# class IPRequest(BaseModel):
#     ip_address: str

# # --- Dependencies ---
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # --- Database Connection Test ---
# @app.on_event("startup")
# def startup_event():
#     try:
#         with engine.connect() as connection:
#             connection.execute(text("SELECT 1"))
#         print("✅ Successfully connected to the PostgreSQL database.")
#     except OperationalError as e:
#         print("❌ Failed to connect to the PostgreSQL database.")
#         print(str(e))

# # --- MikroTik Connection Helper ---
# def connect_to_router():
#     db = SessionLocal()
#     try:
#         device = db.query(MikroTikDevice).first()
#         if not device:
#             raise HTTPException(status_code=404, detail="No MikroTik device configured")
        
#         connection = routeros_api.RouterOsApiPool(
#             host=device.ip_address,
#             username=device.username,
#             password=device.password,
#             port=device.api_port,
#             plaintext_login=True
#         )
#         return connection.get_api()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to connect to router: {str(e)}")
#     finally:
#         db.close()

# # --- API Endpoints ---

# @app.get("/")
# def home():
#     return {"message": "MikroTik Billing API is running", "version": "1.0.0"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy", "database": "connected"}

# # --- MikroTik Router Endpoints ---

# @app.get("/active-users")
# def get_active_users():
#     try:
#         api = connect_to_router()
#         users = api.get_resource('/ip/hotspot/active').get()
#         return {"active_users": users, "count": len(users)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/disconnect-user")
# def disconnect_user(request: IPRequest):
#     try:
#         api = connect_to_router()
#         active = api.get_resource('/ip/hotspot/active')
#         users = active.get()

#         target_user = next((user for user in users if user.get("address") == request.ip_address), None)

#         if not target_user:
#             raise HTTPException(status_code=404, detail="IP address not found in active sessions")

#         active.remove(id=target_user['id'])
#         return {"message": f"User with IP {request.ip_address} has been disconnected"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # --- Package Management Endpoints ---

# @app.get("/packages", response_model=List[PackageResponse])
# def get_packages(db: Session = Depends(get_db)):
#     try:
#         packages = db.query(Package).all()
#         return packages
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/packages", response_model=PackageResponse)
# def create_package(package: PackageCreate, db: Session = Depends(get_db)):
#     try:
#         bandwidth = f"{package.upload_speed}/{package.download_speed}"
        
#         new_package = Package(
#             package_type=package.package_type,
#             name=package.name,
#             session_time=package.session_time,
#             bandwidth=bandwidth,
#             devices=package.devices,
#             price=package.price,
#             data=package.data,
#         )

#         db.add(new_package)
#         db.commit()
#         db.refresh(new_package)
#         return new_package
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.put("/packages/{package_id}", response_model=PackageResponse)
# def update_package(package_id: int, updated_package: PackageUpdate, db: Session = Depends(get_db)):
#     try:
#         package = db.query(Package).filter(Package.id == package_id).first()
#         if not package:
#             raise HTTPException(status_code=404, detail="Package not found")

#         update_data = updated_package.dict(exclude_unset=True)
        
#         # Handle bandwidth update
#         if "upload_speed" in update_data and "download_speed" in update_data:
#             update_data["bandwidth"] = f"{update_data.pop('upload_speed')}/{update_data.pop('download_speed')}"
#         elif "upload_speed" in update_data or "download_speed" in update_data:
#             # If only one speed is provided, we need both to update bandwidth
#             current_speeds = package.bandwidth.split("/")
#             upload = update_data.pop("upload_speed", current_speeds[0])
#             download = update_data.pop("download_speed", current_speeds[1])
#             update_data["bandwidth"] = f"{upload}/{download}"

#         for key, value in update_data.items():
#             setattr(package, key, value)

#         db.commit()
#         db.refresh(package)
#         return package
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/packages/{package_id}")
# def delete_package(package_id: int, db: Session = Depends(get_db)):
#     try:
#         package = db.query(Package).filter(Package.id == package_id).first()
#         if not package:
#             raise HTTPException(status_code=404, detail="Package not found")
        
#         db.delete(package)
#         db.commit()
#         return {"message": "Package deleted successfully"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# # --- User Management Endpoints ---

# @app.get("/users", response_model=List[UserResponse])
# def get_users(db: Session = Depends(get_db)):
#     try:
#         users = db.query(User).all()
#         return users
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/users", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     try:
#         # Check if username already exists
#         existing_user = db.query(User).filter(User.username == user.username).first()
#         if existing_user:
#             raise HTTPException(status_code=400, detail="Username already exists")
        
#         new_user = User(**user.dict())
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except HTTPException:
#         raise
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.put("/users/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
#     try:
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         # Check username uniqueness if updating username
#         if user_update.username and user_update.username != user.username:
#             existing = db.query(User).filter(User.username == user_update.username).first()
#             if existing:
#                 raise HTTPException(status_code=400, detail="Username already exists")

#         for key, value in user_update.dict(exclude_unset=True).items():
#             setattr(user, key, value)

#         db.commit()
#         db.refresh(user)
#         return user
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     try:
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         db.delete(user)
#         db.commit()
#         return {"message": f"User with ID {user_id} deleted successfully"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# # --- MikroTik Device Management Endpoints ---

# @app.get("/mikrotik-devices", response_model=List[MikroTikDeviceResponse])
# def get_devices(db: Session = Depends(get_db)):
#     try:
#         return db.query(MikroTikDevice).all()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/mikrotik-devices", response_model=MikroTikDeviceResponse)
# def create_device(device: MikroTikDeviceCreate, db: Session = Depends(get_db)):
#     try:
#         # Check if device with same IP already exists
#         existing = db.query(MikroTikDevice).filter(MikroTikDevice.ip_address == device.ip_address).first()
#         if existing:
#             raise HTTPException(status_code=400, detail="Device with this IP address already exists")
        
#         new_device = MikroTikDevice(**device.dict())
#         db.add(new_device)
#         db.commit()
#         db.refresh(new_device)
#         return new_device
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/mikrotik-devices/{device_id}")
# def delete_device(device_id: int, db: Session = Depends(get_db)):
#     try:
#         device = db.query(MikroTikDevice).filter(MikroTikDevice.id == device_id).first()
#         if not device:
#             raise HTTPException(status_code=404, detail="Device not found")
        
#         db.delete(device)
#         db.commit()
#         return {"message": "Device deleted successfully"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# # --- Connection Testing Endpoints ---

# @app.post("/test-mikrotik-api")
# def test_mikrotik_api_connection(device: MikroTikDeviceCreate):
#     try:
#         connection = routeros_api.RouterOsApiPool(
#             host=device.ip_address,
#             username=device.username,
#             password=device.password,
#             port=device.api_port,
#             plaintext_login=True
#         )
#         api = connection.get_api()
        
#         # Test connection by fetching system resource
#         api.get_resource('/system/resource').get()
#         connection.disconnect()
        
#         print(f"✅ Successfully connected to MikroTik router at {device.ip_address}")
#         return {"message": "Successfully connected to MikroTik router via API", "status": "success"}
#     except Exception as e:
#         print(f"❌ Connection to MikroTik router at {device.ip_address} failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"API connection failed: {str(e)}")

# @app.post("/test-mikrotik-ssh")
# def test_mikrotik_ssh_connection(device: MikroTikDeviceCreate):
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(
#             hostname=device.ip_address,
#             port=22,  # SSH port
#             username=device.username,
#             password=device.password,
#             timeout=10
#         )
#         ssh.close()
#         return {"message": "Successfully connected via SSH", "status": "success"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"SSH connection failed: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)





























































































































# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, model_validator
# from typing import Optional, Literal, List
# from datetime import date
# import routeros_api
# import paramiko

# from sqlalchemy import create_engine, text, Column, Integer, String, Float, Boolean
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from sqlalchemy.exc import SQLAlchemyError, OperationalError

# # --- FastAPI app ---
# app = FastAPI(title="MikroTik Billing API", version="1.0.0")

# # --- CORS ---

# # Allow localhost frontend
# origins = [
#     "http://localhost:5173",  # Vite default port
#     "http://127.0.0.1:5173"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,            # or ["*"] for all
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- PostgreSQL Database Setup ---
# DATABASE_URL = "postgresql://MikrotikDB_owner:npg_56LBlfUTePyM@ep-wispy-scene-a8v3hj9a-pooler.eastus2.azure.neon.tech/MikrotikDB?sslmode=require"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # --- Database Models ---
# class Package(Base):
#     __tablename__ = "packages"

#     id = Column(Integer, primary_key=True, index=True)
#     package_type = Column(String, nullable=False)   # hotspot, pppoe, dataplan, freetrial
#     name = Column(String, nullable=False)           # e.g. "10mbps unlimited"
#     session_time = Column(String, nullable=False)   # e.g. "1h30m"
#     bandwidth = Column(String, nullable=False)      # e.g. "2M/2M"
#     devices = Column(Integer, nullable=False)
#     price = Column(Float, nullable=False)
#     data = Column(String, nullable=True)            # mandatory only for dataplan

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, nullable=False, unique=True)
#     phone = Column(String, nullable=False)
#     user_type = Column(String, nullable=False)      # "Hotspot" or "PPPoE"
#     package = Column(String, nullable=True)
#     expiry = Column(String, default="Expired")
#     last_online = Column(String, default="Never")
#     password = Column(String, nullable=False)

# class MikroTikDevice(Base):
#     __tablename__ = "mikrotik_devices"

#     id = Column(Integer, primary_key=True, index=True)
#     device_name = Column(String, nullable=False)
#     ip_address = Column(String, nullable=False, unique=True)
#     username = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     connection_method = Column(String, nullable=False, default="api")  # "api" or "ssh"
#     api_port = Column(Integer, default=8728)
#     ssh_port = Column(Integer, default=22)
#     web_port = Column(Integer, default=80)
#     web_enabled = Column(Boolean, default=True)
#     winbox_enabled = Column(Boolean, default=True)
#     ssh_enabled = Column(Boolean, default=False)
#     status = Column(String, default="offline")  # "online", "offline", "unknown"

# # Create DB tables
# Base.metadata.create_all(bind=engine)

# # --- Pydantic Schemas ---
# class PackageCreate(BaseModel):
#     package_type: Literal["hotspot", "pppoe", "dataplan", "freetrial"]
#     name: str
#     session_time: str
#     upload_speed: str
#     download_speed: str
#     devices: int
#     price: float
#     data: Optional[str] = None

#     @model_validator(mode="after")
#     def check_data_for_dataplan(self):
#         if self.package_type == "dataplan" and not self.data:
#             raise ValueError("Data is required for dataplan package type")
#         return self

# class PackageUpdate(BaseModel):
#     package_type: Optional[Literal["hotspot", "pppoe", "dataplan", "freetrial"]] = None
#     name: Optional[str] = None
#     session_time: Optional[str] = None
#     upload_speed: Optional[str] = None
#     download_speed: Optional[str] = None
#     devices: Optional[int] = None
#     price: Optional[float] = None
#     data: Optional[str] = None

# class PackageResponse(BaseModel):
#     id: int
#     package_type: str
#     name: str
#     session_time: str
#     bandwidth: str
#     devices: int
#     price: float
#     data: Optional[str] = None

#     class Config:
#         from_attributes = True

# class UserCreate(BaseModel):
#     username: str
#     phone: str
#     user_type: Literal["Hotspot", "PPPoE"]
#     package: Optional[str] = None
#     expiry: Optional[str] = "Expired"
#     last_online: Optional[str] = "Never"
#     password: str

# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     phone: Optional[str] = None
#     user_type: Optional[Literal["Hotspot", "PPPoE"]] = None
#     package: Optional[str] = None
#     expiry: Optional[str] = None
#     last_online: Optional[str] = None
#     password: Optional[str] = None

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     phone: str
#     user_type: str
#     package: Optional[str] = None
#     expiry: str
#     last_online: str
#     password: str

#     class Config:
#         from_attributes = True

# # Updated MikroTik Device Schemas to match frontend
# class MikroTikDeviceCreate(BaseModel):
#     device_name: str
#     ip_address: str
#     username: str
#     password: str
#     connection_method: Literal["api", "ssh"] = "api"
#     api_port: Optional[int] = 8728
#     ssh_port: Optional[int] = 22
#     web_port: Optional[int] = 80
#     web_enabled: Optional[bool] = True
#     winbox_enabled: Optional[bool] = True
#     ssh_enabled: Optional[bool] = False
#     status: Optional[str] = "offline"

# class MikroTikDeviceResponse(BaseModel):
#     id: int
#     device_name: str
#     ip_address: str
#     username: str
#     password: str
#     connection_method: str
#     api_port: Optional[int]
#     ssh_port: Optional[int]
#     web_port: Optional[int]
#     web_enabled: Optional[bool]
#     winbox_enabled: Optional[bool]
#     ssh_enabled: Optional[bool]
#     status: Optional[str]

#     class Config:
#         from_attributes = True

# # Test connection schemas (matching frontend requests)
# class MikroTikAPITestRequest(BaseModel):
#     host: str
#     username: str
#     password: str
#     port: int

# class MikroTikSSHTestRequest(BaseModel):
#     ip_address: str
#     username: str
#     password: str
#     port: int

# class IPRequest(BaseModel):
#     ip_address: str

# # --- Dependencies ---
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # --- Database Connection Test ---
# @app.on_event("startup")
# def startup_event():
#     try:
#         with engine.connect() as connection:
#             connection.execute(text("SELECT 1"))
#         print("✅ Successfully connected to the PostgreSQL database.")
#     except OperationalError as e:
#         print("❌ Failed to connect to the PostgreSQL database.")
#         print(str(e))

# # --- MikroTik Connection Helper ---
# def connect_to_router():
#     db = SessionLocal()
#     try:
#         device = db.query(MikroTikDevice).first()
#         if not device:
#             raise HTTPException(status_code=404, detail="No MikroTik device configured")
        
#         if device.connection_method == "api":
#             connection = routeros_api.RouterOsApiPool(
#                 host=device.ip_address,
#                 username=device.username,
#                 password=device.password,
#                 port=device.api_port,
#                 plaintext_login=True
#             )
#             return connection.get_api()
#         else:
#             raise HTTPException(status_code=400, detail="SSH connection not supported for this operation")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to connect to router: {str(e)}")
#     finally:
#         db.close()

# # --- API Endpoints ---

# @app.get("/")
# def home():
#     return {"message": "MikroTik Billing API is running", "version": "1.0.0"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy", "database": "connected"}

# # --- MikroTik Router Endpoints ---

# @app.get("/active-users")
# def get_active_users():
#     try:
#         api = connect_to_router()
#         users = api.get_resource('/ip/hotspot/active').get()
#         return {"active_users": users, "count": len(users)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/disconnect-user")
# def disconnect_user(request: IPRequest):
#     try:
#         api = connect_to_router()
#         active = api.get_resource('/ip/hotspot/active')
#         users = active.get()

#         target_user = next((user for user in users if user.get("address") == request.ip_address), None)

#         if not target_user:
#             raise HTTPException(status_code=404, detail="IP address not found in active sessions")

#         active.remove(id=target_user['id'])
#         return {"message": f"User with IP {request.ip_address} has been disconnected"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # --- Package Management Endpoints ---

# @app.get("/packages", response_model=List[PackageResponse])
# def get_packages(db: Session = Depends(get_db)):
#     try:
#         packages = db.query(Package).all()
#         return packages
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/packages", response_model=PackageResponse)
# def create_package(package: PackageCreate, db: Session = Depends(get_db)):
#     try:
#         bandwidth = f"{package.upload_speed}/{package.download_speed}"
        
#         new_package = Package(
#             package_type=package.package_type,
#             name=package.name,
#             session_time=package.session_time,
#             bandwidth=bandwidth,
#             devices=package.devices,
#             price=package.price,
#             data=package.data,
#         )

#         db.add(new_package)
#         db.commit()
#         db.refresh(new_package)
#         return new_package
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.put("/packages/{package_id}", response_model=PackageResponse)
# def update_package(package_id: int, updated_package: PackageUpdate, db: Session = Depends(get_db)):
#     try:
#         package = db.query(Package).filter(Package.id == package_id).first()
#         if not package:
#             raise HTTPException(status_code=404, detail="Package not found")

#         update_data = updated_package.dict(exclude_unset=True)
        
#         # Handle bandwidth update
#         if "upload_speed" in update_data and "download_speed" in update_data:
#             update_data["bandwidth"] = f"{update_data.pop('upload_speed')}/{update_data.pop('download_speed')}"
#         elif "upload_speed" in update_data or "download_speed" in update_data:
#             # If only one speed is provided, we need both to update bandwidth
#             current_speeds = package.bandwidth.split("/")
#             upload = update_data.pop("upload_speed", current_speeds[0])
#             download = update_data.pop("download_speed", current_speeds[1])
#             update_data["bandwidth"] = f"{upload}/{download}"

#         for key, value in update_data.items():
#             setattr(package, key, value)

#         db.commit()
#         db.refresh(package)
#         return package
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/packages/{package_id}")
# def delete_package(package_id: int, db: Session = Depends(get_db)):
#     try:
#         package = db.query(Package).filter(Package.id == package_id).first()
#         if not package:
#             raise HTTPException(status_code=404, detail="Package not found")
        
#         db.delete(package)
#         db.commit()
#         return {"message": "Package deleted successfully"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
    



# # --- User Management Endpoints ---

# # @app.get("/users", response_model=List[UserResponse])
# # def get_users(db: Session = Depends(get_db)):
# #     try:
# #         users = db.query(User).all()
# #         return users
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))



# @app.get("/users", response_model=List[UserResponse])
# def get_users(db: Session = Depends(get_db)):
#     try:
#         users = db.query(User).all()
#         return [
#             {
#                 "id": user.id,
#                 "username": user.username,
#                 "phone": user.phone,
#                 "user_type": user.user_type,
#                 "package": user.package,
#                 "expiry": user.expiry.isoformat() if hasattr(user.expiry, "isoformat") else user.expiry,
#                 "last_online": user.last_online,
#             }
#             for user in users
#         ]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/users", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     try:
#         # Check if username already exists
#         existing_user = db.query(User).filter(User.username == user.username).first()
#         if existing_user:
#             raise HTTPException(status_code=400, detail="Username already exists")
        
#         new_user = User(**user.dict())
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except HTTPException:
#         raise
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# @app.put("/users/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
#     try:
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         # Check username uniqueness if updating username
#         if user_update.username and user_update.username != user.username:
#             existing = db.query(User).filter(User.username == user_update.username).first()
#             if existing:
#                 raise HTTPException(status_code=400, detail="Username already exists")

#         for key, value in user_update.dict(exclude_unset=True).items():
#             setattr(user, key, value)

#         db.commit()
#         db.refresh(user)
#         return user
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     try:
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         db.delete(user)
#         db.commit()
#         return {"message": f"User with ID {user_id} deleted successfully"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# # --- MikroTik Device Management Endpoints ---

# @app.get("/mikrotik-devices", response_model=List[MikroTikDeviceResponse])
# def get_devices(db: Session = Depends(get_db)):
#     try:
#         return db.query(MikroTikDevice).all()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Updated endpoint to match frontend URL and handle comprehensive device data
# @app.post("/link-mikrotik", response_model=MikroTikDeviceResponse)
# def link_mikrotik_device(device: MikroTikDeviceCreate, db: Session = Depends(get_db)):
#     try:
#         # Check if device with same IP already exists
#         existing = db.query(MikroTikDevice).filter(MikroTikDevice.ip_address == device.ip_address).first()
#         if existing:
#             raise HTTPException(status_code=400, detail="Device with this IP address already exists")
        
#         # Check if device name already exists
#         existing_name = db.query(MikroTikDevice).filter(MikroTikDevice.device_name == device.device_name).first()
#         if existing_name:
#             raise HTTPException(status_code=400, detail="Device with this name already exists")
        
#         new_device = MikroTikDevice(**device.dict())
#         db.add(new_device)
#         db.commit()
#         db.refresh(new_device)
#         return new_device
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/mikrotik-devices/{device_id}")
# def delete_device(device_id: int, db: Session = Depends(get_db)):
#     try:
#         device = db.query(MikroTikDevice).filter(MikroTikDevice.id == device_id).first()
#         if not device:
#             raise HTTPException(status_code=404, detail="Device not found")
        
#         db.delete(device)
#         db.commit()
#         return {"message": "Device deleted successfully"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# # --- Connection Testing Endpoints (Updated to match frontend requests) ---

# @app.post("/test-mikrotik-connection")
# def test_mikrotik_api_connection(device: MikroTikAPITestRequest):
#     try:
#         connection = routeros_api.RouterOsApiPool(
#             host=device.host,
#             username=device.username,
#             password=device.password,
#             port=device.port,
#             plaintext_login=True
#         )
#         api = connection.get_api()
        
#         # Test connection by fetching system resource
#         system_info = api.get_resource('/system/resource').get()
#         connection.disconnect()
        
#         print(f"✅ Successfully connected to MikroTik router at {device.host}")
#         return {
#             "message": "Successfully connected to MikroTik router via API", 
#             "status": "success",
#             "success": True,
#             "system_info": system_info[0] if system_info else None
#         }
#     except Exception as e:
#         print(f"❌ Connection to MikroTik router at {device.host} failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"API connection failed: {str(e)}")

# @app.post("/test-mikrotik-ssh-connection")
# def test_mikrotik_ssh_connection(device: MikroTikSSHTestRequest):
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(
#             hostname=device.ip_address,
#             port=device.port,
#             username=device.username,
#             password=device.password,
#             timeout=10
#         )
        
#         # Test by executing a simple command
#         stdin, stdout, stderr = ssh.exec_command('/system resource print')
#         output = stdout.read().decode()
#         ssh.close()
        
#         return {
#             "message": "Successfully connected via SSH", 
#             "status": "success",
#             "success": True,
#             "output": output[:200] + "..." if len(output) > 200 else output
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"SSH connection failed: {str(e)}")

# # Update device status endpoint
# @app.put("/mikrotik-devices/{device_id}/status")
# def update_device_status(device_id: int, status: str, db: Session = Depends(get_db)):
#     try:
#         device = db.query(MikroTikDevice).filter(MikroTikDevice.id == device_id).first()
#         if not device:
#             raise HTTPException(status_code=404, detail="Device not found")
        
#         device.status = status
#         db.commit()
#         db.refresh(device)
#         return {"message": f"Device status updated to {status}", "device": device}
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)













from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, model_validator
from typing import Optional, Literal, List
from datetime import date
import routeros_api
import paramiko

from sqlalchemy import create_engine, text, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# --- FastAPI app ---
app = FastAPI(title="MikroTik Billing API", version="1.0.0")

# --- CORS ---


# Allow your frontend origin
origins = [
    "https://mikrotikcaptive.netlify.app",
    "https://zoomocaptivepg.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", origins],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

# --- PostgreSQL Database Setup ---
DATABASE_URL = "postgresql://MikrotikDB_owner:npg_56LBlfUTePyM@ep-wispy-scene-a8v3hj9a-pooler.eastus2.azure.neon.tech/MikrotikDB?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Models ---
class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    package_type = Column(String, nullable=False)   # hotspot, pppoe, dataplan, freetrial
    name = Column(String, nullable=False)           # e.g. "10mbps unlimited"
    session_time = Column(String, nullable=False)   # e.g. "1h30m"
    bandwidth = Column(String, nullable=False)      # e.g. "2M/2M"
    devices = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    data = Column(String, nullable=True)            # mandatory only for dataplan

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    user_type = Column(String, nullable=False)      # "Hotspot" or "PPPoE"
    package = Column(String, nullable=True)
    expiry = Column(String, default="Expired")
    last_online = Column(String, default="Never")
    password = Column(String, nullable=False)

class MikroTikDevice(Base):
    __tablename__ = "mikrotik_devices"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    connection_method = Column(String, nullable=False, default="api")  # "api" or "ssh"
    api_port = Column(Integer, default=8728)
    ssh_port = Column(Integer, default=22)
    web_port = Column(Integer, default=80)
    web_enabled = Column(Boolean, default=True)
    winbox_enabled = Column(Boolean, default=True)
    ssh_enabled = Column(Boolean, default=False)
    status = Column(String, default="offline")  # "online", "offline", "unknown"

# Create DB tables
Base.metadata.create_all(bind=engine)

# --- Pydantic Schemas ---
class PackageCreate(BaseModel):
    package_type: Literal["hotspot", "pppoe", "dataplan", "freetrial"]
    name: str
    session_time: str
    upload_speed: str
    download_speed: str
    devices: int
    price: float
    data: Optional[str] = None

    @model_validator(mode="after")
    def check_data_for_dataplan(self):
        if self.package_type == "dataplan" and not self.data:
            raise ValueError("Data is required for dataplan package type")
        return self

class PackageUpdate(BaseModel):
    package_type: Optional[Literal["hotspot", "pppoe", "dataplan", "freetrial"]] = None
    name: Optional[str] = None
    session_time: Optional[str] = None
    upload_speed: Optional[str] = None
    download_speed: Optional[str] = None
    devices: Optional[int] = None
    price: Optional[float] = None
    data: Optional[str] = None

class PackageResponse(BaseModel):
    id: int
    package_type: str
    name: str
    session_time: str
    bandwidth: str
    devices: int
    price: float
    data: Optional[str] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    phone: str
    user_type: Literal["Hotspot", "PPPoE"]
    package: Optional[str] = None
    expiry: Optional[str] = "Expired"
    last_online: Optional[str] = "Never"
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    user_type: Optional[Literal["Hotspot", "PPPoE"]] = None
    package: Optional[str] = None
    expiry: Optional[str] = None
    last_online: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    phone: str
    user_type: str
    package: Optional[str]
    expiry: Optional[date] 
    last_online: Optional[str]
    password: str

class Config:
    from_attributes = True

# Updated MikroTik Device Schemas to match frontend
class MikroTikDeviceCreate(BaseModel):
    device_name: str
    ip_address: str
    username: str
    password: str
    connection_method: Literal["api", "ssh"] = "api"
    api_port: Optional[int] = 8728
    ssh_port: Optional[int] = 22
    web_port: Optional[int] = 80
    web_enabled: Optional[bool] = True
    winbox_enabled: Optional[bool] = True
    ssh_enabled: Optional[bool] = False
    status: Optional[str] = "offline"

class MikroTikDeviceResponse(BaseModel):
    id: int
    device_name: str
    ip_address: str
    username: str
    password: str
    connection_method: str
    api_port: Optional[int]
    ssh_port: Optional[int]
    web_port: Optional[int]
    web_enabled: Optional[bool]
    winbox_enabled: Optional[bool]
    ssh_enabled: Optional[bool]
    status: str
    # Real-time system information
    board_name: Optional[str] = None
    cpu_load: Optional[str] = None
    memory_usage: Optional[str] = None
    total_memory: Optional[str] = None
    free_memory: Optional[str] = None
    uptime: Optional[str] = None
    version: Optional[str] = None
    architecture: Optional[str] = None
    web_service_status: Optional[str] = None
    winbox_service_status: Optional[str] = None
    ssh_service_status: Optional[str] = None

    class Config:
        from_attributes = True

# Test connection schemas (matching frontend requests)
class MikroTikAPITestRequest(BaseModel):
    host: str
    username: str
    password: str
    port: int

class MikroTikSSHTestRequest(BaseModel):
    ip_address: str
    username: str
    password: str
    port: int

class IPRequest(BaseModel):
    ip_address: str

# --- Dependencies ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Database Connection Test ---
@app.on_event("startup")
def startup_event():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Successfully connected to the PostgreSQL database.")
    except OperationalError as e:
        print("❌ Failed to connect to the PostgreSQL database.")
        print(str(e))

# --- MikroTik Connection Helper ---
def connect_to_router():
    db = SessionLocal()
    try:
        device = db.query(MikroTikDevice).first()
        if not device:
            raise HTTPException(status_code=404, detail="No MikroTik device configured")
        
        if device.connection_method == "api":
            connection = routeros_api.RouterOsApiPool(
                host=device.ip_address,
                username=device.username,
                password=device.password,
                port=device.api_port,
                plaintext_login=True
            )
            return connection.get_api()
        else:
            raise HTTPException(status_code=400, detail="SSH connection not supported for this operation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to router: {str(e)}")
    finally:
        db.close()

# --- API Endpoints ---

@app.get("/")
def home():
    return {"message": "MikroTik Billing API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

# --- MikroTik Router Endpoints ---

@app.get("/active-users")
def get_active_users():
    try:
        api = connect_to_router()
        users = api.get_resource('/ip/hotspot/active').get()
        return {"active_users": users, "count": len(users)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/disconnect-user")
def disconnect_user(request: IPRequest):
    try:
        api = connect_to_router()
        active = api.get_resource('/ip/hotspot/active')
        users = active.get()

        target_user = next((user for user in users if user.get("address") == request.ip_address), None)

        if not target_user:
            raise HTTPException(status_code=404, detail="IP address not found in active sessions")

        active.remove(id=target_user['id'])
        return {"message": f"User with IP {request.ip_address} has been disconnected"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Package Management Endpoints ---

@app.get("/packages", response_model=List[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    try:
        packages = db.query(Package).all()
        return packages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/packages", response_model=PackageResponse)
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    try:
        bandwidth = f"{package.upload_speed}/{package.download_speed}"
        
        new_package = Package(
            package_type=package.package_type,
            name=package.name,
            session_time=package.session_time,
            bandwidth=bandwidth,
            devices=package.devices,
            price=package.price,
            data=package.data,
        )

        db.add(new_package)
        db.commit()
        db.refresh(new_package)
        return new_package
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/packages/{package_id}", response_model=PackageResponse)
def update_package(package_id: int, updated_package: PackageUpdate, db: Session = Depends(get_db)):
    try:
        package = db.query(Package).filter(Package.id == package_id).first()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")

        update_data = updated_package.dict(exclude_unset=True)
        
        # Handle bandwidth update
        if "upload_speed" in update_data and "download_speed" in update_data:
            update_data["bandwidth"] = f"{update_data.pop('upload_speed')}/{update_data.pop('download_speed')}"
        elif "upload_speed" in update_data or "download_speed" in update_data:
            # If only one speed is provided, we need both to update bandwidth
            current_speeds = package.bandwidth.split("/")
            upload = update_data.pop("upload_speed", current_speeds[0])
            download = update_data.pop("download_speed", current_speeds[1])
            update_data["bandwidth"] = f"{upload}/{download}"

        for key, value in update_data.items():
            setattr(package, key, value)

        db.commit()
        db.refresh(package)
        return package
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/packages/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    try:
        package = db.query(Package).filter(Package.id == package_id).first()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        
        db.delete(package)
        db.commit()
        return {"message": "Package deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- User Management Endpoints ---

@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        new_user = User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check username uniqueness if updating username
        if user_update.username and user_update.username != user.username:
            existing = db.query(User).filter(User.username == user_update.username).first()
            if existing:
                raise HTTPException(status_code=400, detail="Username already exists")

        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": f"User with ID {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- MikroTik Device Management Endpoints ---

@app.get("/mikrotik-devices", response_model=List[MikroTikDeviceResponse])
def get_devices(db: Session = Depends(get_db)):
    try:
        devices = db.query(MikroTikDevice).all()
        enhanced_devices = []
        
        for device in devices:
            device_data = {
                "id": device.id,
                "device_name": device.device_name,
                "ip_address": device.ip_address,
                "username": device.username,
                "password": device.password,
                "connection_method": device.connection_method,
                "api_port": device.api_port,
                "ssh_port": device.ssh_port,
                "web_port": device.web_port,
                "web_enabled": device.web_enabled,
                "winbox_enabled": device.winbox_enabled,
                "ssh_enabled": device.ssh_enabled,
                "status": "offline",
                "board_name": None,
                "cpu_load": None,
                "memory_usage": None,
                "total_memory": None,
                "free_memory": None,
                "uptime": None,
                "version": None,
                "architecture": None,
                "web_service_status": "unknown",
                "winbox_service_status": "unknown",
                "ssh_service_status": "unknown"
            }
            
            # Try to connect and get real-time information
            if device.connection_method == "api":
                try:
                    connection = routeros_api.RouterOsApiPool(
                        host=device.ip_address,
                        username=device.username,
                        password=device.password,
                        port=device.api_port,
                        plaintext_login=True
                    )
                    api = connection.get_api()
                    
                    # Get system resource information
                    try:
                        resource_info = api.get_resource('/system/resource').get()
                        if resource_info:
                            resource = resource_info[0]
                            device_data["cpu_load"] = resource.get("cpu-load", "0") + "%"
                            
                            # Memory calculations
                            total_mem = int(resource.get("total-memory", 0))
                            free_mem = int(resource.get("free-memory", 0))
                            used_mem = total_mem - free_mem
                            
                            device_data["total_memory"] = f"{total_mem // (1024*1024)} MB"
                            device_data["free_memory"] = f"{free_mem // (1024*1024)} MB"
                            device_data["memory_usage"] = f"{(used_mem/total_mem*100):.1f}%" if total_mem > 0 else "0%"
                            device_data["uptime"] = resource.get("uptime", "Unknown")
                            device_data["version"] = resource.get("version", "Unknown")
                            device_data["architecture"] = resource.get("architecture-name", "Unknown")
                    except Exception as e:
                        print(f"Failed to get resource info for {device.ip_address}: {e}")
                    
                    # Get system identity (board name)
                    try:
                        identity_info = api.get_resource('/system/identity').get()
                        if identity_info:
                            device_data["board_name"] = identity_info[0].get("name", "Unknown")
                    except Exception as e:
                        print(f"Failed to get identity for {device.ip_address}: {e}")
                        device_data["board_name"] = device.device_name  # Fallback to device name
                    
                    # Get service status
                    try:
                        services = api.get_resource('/ip/service').get()
                        for service in services:
                            service_name = service.get("name", "")
                            is_disabled = service.get("disabled", "false") == "true"
                            status = "disabled" if is_disabled else "enabled"
                            
                            if service_name == "www":
                                device_data["web_service_status"] = status
                            elif service_name == "winbox":
                                device_data["winbox_service_status"] = status
                            elif service_name == "ssh":
                                device_data["ssh_service_status"] = status
                    except Exception as e:
                        print(f"Failed to get service status for {device.ip_address}: {e}")
                    
                    # If we got here, connection was successful
                    device_data["status"] = "online"
                    
                    # Update device status in database
                    device.status = "online"
                    db.commit()
                    
                    connection.disconnect()
                    
                except Exception as e:
                    print(f"Failed to connect to {device.ip_address}: {e}")
                    device_data["status"] = "offline"
                    device_data["board_name"] = device.device_name  # Fallback to device name
                    
                    # Update device status in database
                    device.status = "offline"
                    db.commit()
            
            elif device.connection_method == "ssh":
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(
                        hostname=device.ip_address,
                        port=device.ssh_port,
                        username=device.username,
                        password=device.password,
                        timeout=10
                    )
                    
                    # Get system resource via SSH
                    try:
                        stdin, stdout, stderr = ssh.exec_command('/system resource print')
                        output = stdout.read().decode()
                        
                        # Parse SSH output (basic parsing)
                        lines = output.split('\n')
                        for line in lines:
                            if 'cpu-load:' in line:
                                device_data["cpu_load"] = line.split('cpu-load:')[1].strip()
                            elif 'free-memory:' in line:
                                free_mem = line.split('free-memory:')[1].strip()
                                device_data["free_memory"] = free_mem
                            elif 'total-memory:' in line:
                                total_mem = line.split('total-memory:')[1].strip()
                                device_data["total_memory"] = total_mem
                            elif 'uptime:' in line:
                                device_data["uptime"] = line.split('uptime:')[1].strip()
                            elif 'version:' in line:
                                device_data["version"] = line.split('version:')[1].strip()
                    except Exception as e:
                        print(f"Failed to get resource info via SSH for {device.ip_address}: {e}")
                    
                    # Get identity via SSH
                    try:
                        stdin, stdout, stderr = ssh.exec_command('/system identity print')
                        output = stdout.read().decode()
                        if 'name:' in output:
                            device_data["board_name"] = output.split('name:')[1].strip().split('\n')[0]
                    except Exception as e:
                        print(f"Failed to get identity via SSH for {device.ip_address}: {e}")
                        device_data["board_name"] = device.device_name
                    
                    # Get service status via SSH
                    try:
                        stdin, stdout, stderr = ssh.exec_command('/ip service print')
                        output = stdout.read().decode()
                        
                        device_data["web_service_status"] = "enabled" if "www" in output and "X" not in output else "disabled"
                        device_data["winbox_service_status"] = "enabled" if "winbox" in output and "X" not in output else "disabled"
                        device_data["ssh_service_status"] = "enabled" if "ssh" in output and "X" not in output else "disabled"
                    except Exception as e:
                        print(f"Failed to get service status via SSH for {device.ip_address}: {e}")
                    
                    device_data["status"] = "online"
                    device.status = "online"
                    db.commit()
                    
                    ssh.close()
                    
                except Exception as e:
                    print(f"Failed to connect via SSH to {device.ip_address}: {e}")
                    device_data["status"] = "offline"
                    device_data["board_name"] = device.device_name
                    device.status = "offline"
                    db.commit()
            
            enhanced_devices.append(MikroTikDeviceResponse(**device_data))
        
        return enhanced_devices
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Updated endpoint to match frontend URL and handle comprehensive device data
@app.post("/link-mikrotik", response_model=MikroTikDeviceResponse)
def link_mikrotik_device(device: MikroTikDeviceCreate, db: Session = Depends(get_db)):
    try:
        # Check if device with same IP already exists
        existing = db.query(MikroTikDevice).filter(MikroTikDevice.ip_address == device.ip_address).first()
        if existing:
            raise HTTPException(status_code=400, detail="Device with this IP address already exists")
        
        # Check if device name already exists
        existing_name = db.query(MikroTikDevice).filter(MikroTikDevice.device_name == device.device_name).first()
        if existing_name:
            raise HTTPException(status_code=400, detail="Device with this name already exists")
        
        new_device = MikroTikDevice(**device.dict())
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return new_device
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/mikrotik-devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    try:
        device = db.query(MikroTikDevice).filter(MikroTikDevice.id == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        db.delete(device)
        db.commit()
        return {"message": "Device deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- Connection Testing Endpoints (Updated to match frontend requests) ---

@app.post("/test-mikrotik-connection")
def test_mikrotik_api_connection(device: MikroTikAPITestRequest):
    try:
        connection = routeros_api.RouterOsApiPool(
            host=device.host,
            username=device.username,
            password=device.password,
            port=device.port,
            plaintext_login=True
        )
        api = connection.get_api()
        
        # Test connection by fetching system resource
        system_info = api.get_resource('/system/resource').get()
        connection.disconnect()
        
        print(f"✅ Successfully connected to MikroTik router at {device.host}")
        return {
            "message": "Successfully connected to MikroTik router via API", 
            "status": "success",
            "success": True,
            "system_info": system_info[0] if system_info else None
        }
    except Exception as e:
        print(f"❌ Connection to MikroTik router at {device.host} failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"API connection failed: {str(e)}")

@app.post("/test-mikrotik-ssh-connection")
def test_mikrotik_ssh_connection(device: MikroTikSSHTestRequest):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=device.ip_address,
            port=device.port,
            username=device.username,
            password=device.password,
            timeout=10
        )
        
        # Test by executing a simple command
        stdin, stdout, stderr = ssh.exec_command('/system resource print')
        output = stdout.read().decode()
        ssh.close()
        
        return {
            "message": "Successfully connected via SSH", 
            "status": "success",
            "success": True,
            "output": output[:200] + "..." if len(output) > 200 else output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SSH connection failed: {str(e)}")

# Update device status endpoint
@app.put("/mikrotik-devices/{device_id}/status")
def update_device_status(device_id: int, status: str, db: Session = Depends(get_db)):
    try:
        device = db.query(MikroTikDevice).filter(MikroTikDevice.id == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        device.status = status
        db.commit()
        db.refresh(device)
        return {"message": f"Device status updated to {status}", "device": device}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def format_memory(bytes_value):
    """Convert bytes to human readable format"""
    try:
        bytes_val = int(bytes_value)
        if bytes_val >= 1024 * 1024 * 1024:
            return f"{bytes_val / (1024 * 1024 * 1024):.1f} GB"
        elif bytes_val >= 1024 * 1024:
            return f"{bytes_val / (1024 * 1024):.0f} MB"
        elif bytes_val >= 1024:
            return f"{bytes_val / 1024:.0f} KB"
        else:
            return f"{bytes_val} B"
    except:
        return str(bytes_value)

@app.get("/mikrotik-devices/{device_id}/refresh", response_model=MikroTikDeviceResponse)
def refresh_device_info(device_id: int, db: Session = Depends(get_db)):
    """Refresh real-time information for a specific device"""
    try:
        device = db.query(MikroTikDevice).filter(MikroTikDevice.id == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Use the same logic as get_devices but for a single device
        devices = [device]
        enhanced_devices = []
        
        for device in devices:
            device_data = {
                "id": device.id,
                "device_name": device.device_name,
                "ip_address": device.ip_address,
                "username": device.username,
                "password": device.password,
                "connection_method": device.connection_method,
                "api_port": device.api_port,
                "ssh_port": device.ssh_port,
                "web_port": device.web_port,
                "web_enabled": device.web_enabled,
                "winbox_enabled": device.winbox_enabled,
                "ssh_enabled": device.ssh_enabled,
                "status": "offline",
                "board_name": None,
                "cpu_load": None,
                "memory_usage": None,
                "total_memory": None,
                "free_memory": None,
                "uptime": None,
                "version": None,
                "architecture": None,
                "web_service_status": "unknown",
                "winbox_service_status": "unknown",
                "ssh_service_status": "unknown"
            }
            
            # Try to connect and get real-time information
            if device.connection_method == "api":
                try:
                    connection = routeros_api.RouterOsApiPool(
                        host=device.ip_address,
                        username=device.username,
                        password=device.password,
                        port=device.api_port,
                        plaintext_login=True
                    )
                    api = connection.get_api()
                    
                    # Get system resource information
                    try:
                        resource_info = api.get_resource('/system/resource').get()
                        if resource_info:
                            resource = resource_info[0]
                            device_data["cpu_load"] = resource.get("cpu-load", "0") + "%"
                            
                            # Memory calculations
                            total_mem = int(resource.get("total-memory", 0))
                            free_mem = int(resource.get("free-memory", 0))
                            used_mem = total_mem - free_mem
                            
                            device_data["total_memory"] = f"{total_mem // (1024*1024)} MB"
                            device_data["free_memory"] = f"{free_mem // (1024*1024)} MB"
                            device_data["memory_usage"] = f"{(used_mem/total_mem*100):.1f}%" if total_mem > 0 else "0%"
                            device_data["uptime"] = resource.get("uptime", "Unknown")
                            device_data["version"] = resource.get("version", "Unknown")
                            device_data["architecture"] = resource.get("architecture-name", "Unknown")
                    except Exception as e:
                        print(f"Failed to get resource info for {device.ip_address}: {e}")
                    
                    # Get system identity (board name)
                    try:
                        identity_info = api.get_resource('/system/identity').get()
                        if identity_info:
                            device_data["board_name"] = identity_info[0].get("name", "Unknown")
                    except Exception as e:
                        print(f"Failed to get identity for {device.ip_address}: {e}")
                        device_data["board_name"] = device.device_name  # Fallback to device name
                    
                    # Get service status
                    try:
                        services = api.get_resource('/ip/service').get()
                        for service in services:
                            service_name = service.get("name", "")
                            is_disabled = service.get("disabled", "false") == "true"
                            status = "disabled" if is_disabled else "enabled"
                            
                            if service_name == "www":
                                device_data["web_service_status"] = status
                            elif service_name == "winbox":
                                device_data["winbox_service_status"] = status
                            elif service_name == "ssh":
                                device_data["ssh_service_status"] = status
                    except Exception as e:
                        print(f"Failed to get service status for {device.ip_address}: {e}")
                    
                    # If we got here, connection was successful
                    device_data["status"] = "online"
                    
                    # Update device status in database
                    device.status = "online"
                    db.commit()
                    
                    connection.disconnect()
                    
                except Exception as e:
                    print(f"Failed to connect to {device.ip_address}: {e}")
                    device_data["status"] = "offline"
                    device_data["board_name"] = device.device_name  # Fallback to device name
                    
                    # Update device status in database
                    device.status = "offline"
                    db.commit()
            
            elif device.connection_method == "ssh":
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(
                        hostname=device.ip_address,
                        port=device.ssh_port,
                        username=device.username,
                        password=device.password,
                        timeout=10
                    )
                    
                    # Get system resource via SSH
                    try:
                        stdin, stdout, stderr = ssh.exec_command('/system resource print')
                        output = stdout.read().decode()
                        
                        # Parse SSH output (basic parsing)
                        lines = output.split('\n')
                        for line in lines:
                            if 'cpu-load:' in line:
                                device_data["cpu_load"] = line.split('cpu-load:')[1].strip()
                            elif 'free-memory:' in line:
                                free_mem = line.split('free-memory:')[1].strip()
                                device_data["free_memory"] = free_mem
                            elif 'total-memory:' in line:
                                total_mem = line.split('total-memory:')[1].strip()
                                device_data["total_memory"] = total_mem
                            elif 'uptime:' in line:
                                device_data["uptime"] = line.split('uptime:')[1].strip()
                            elif 'version:' in line:
                                device_data["version"] = line.split('version:')[1].strip()
                    except Exception as e:
                        print(f"Failed to get resource info via SSH for {device.ip_address}: {e}")
                    
                    # Get identity via SSH
                    try:
                        stdin, stdout, stderr = ssh.exec_command('/system identity print')
                        output = stdout.read().decode()
                        if 'name:' in output:
                            device_data["board_name"] = output.split('name:')[1].strip().split('\n')[0]
                    except Exception as e:
                        print(f"Failed to get identity via SSH for {device.ip_address}: {e}")
                        device_data["board_name"] = device.device_name
                    
                    # Get service status via SSH
                    try:
                        stdin, stdout, stderr = ssh.exec_command('/ip service print')
                        output = stdout.read().decode()
                        
                        device_data["web_service_status"] = "enabled" if "www" in output and "X" not in output else "disabled"
                        device_data["winbox_service_status"] = "enabled" if "winbox" in output and "X" not in output else "disabled"
                        device_data["ssh_service_status"] = "enabled" if "ssh" in output and "X" not in output else "disabled"
                    except Exception as e:
                        print(f"Failed to get service status via SSH for {device.ip_address}: {e}")
                    
                    device_data["status"] = "online"
                    device.status = "online"
                    db.commit()
                    
                    ssh.close()
                    
                except Exception as e:
                    print(f"Failed to connect via SSH to {device.ip_address}: {e}")
                    device_data["status"] = "offline"
                    device_data["board_name"] = device.device_name
                    device.status = "offline"
                    db.commit()
            
            enhanced_devices.append(MikroTikDeviceResponse(**device_data))
        
        return enhanced_devices[0] if enhanced_devices else None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
