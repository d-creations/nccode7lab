import platform
import asyncio
import json
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from .interface import ProtocolClient, TransferError
from . import get_transfer_client

router = APIRouter(prefix="/api/transfer", tags=["transfer"])

class TransferConnection(BaseModel):
    ip_address: str
    protocol: str
    port: Optional[int] = None
    timeout: int = 10
    driver_path: Optional[str] = None  # Absolute path to DLLs if applicable

class TransferDownloadData(BaseModel):
    program_text: str
    protocol: str
    port: Optional[int] = None
    driver_path: Optional[str] = None
    file_extension: Optional[str] = None  # Machine-config-derived file extension (e.g. ".P1", ".p-2", ".PA", "")

def get_client(protocol: str, driver_path: Optional[str] = None) -> ProtocolClient:
    try:
        return get_transfer_client(protocol, driver_path)
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Transfer protocol error: {e}")

def parse_file_extensions(value: Optional[str]) -> Optional[list[str]]:
    if value is None:
        return None
    try:
        extensions = json.loads(value)
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=400, detail="file_extensions must be a JSON array") from error
    if not isinstance(extensions, list) or not all(isinstance(extension, str) for extension in extensions):
        raise HTTPException(status_code=400, detail="file_extensions must be a JSON array of strings")
    return extensions

@router.get("/ping")
async def transfer_ping(ip_address: str, protocol: Optional[str] = None, driver_path: Optional[str] = None):
    if (protocol or "").lower() == "usb":
        client = get_client("usb", driver_path)
        try:
            return {"status": "success", "available": client.connect(ip_address)}
        finally:
            client.disconnect()

    is_windows = platform.system().lower() == "windows"
    param_count = "-n" if is_windows else "-c"
    param_wait = "-w" if is_windows else "-W"
    wait_val = "1000" if is_windows else "1"
    
    try:
        process = await asyncio.create_subprocess_exec(
            "ping", param_count, "1", param_wait, wait_val, ip_address,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        return {"status": "success", "available": process.returncode == 0}
    except Exception as e:
        return {"status": "success", "available": False, "error": str(e)}

@router.post("/connect")
async def transfer_connect(conn: TransferConnection):
    client = get_client(conn.protocol, conn.driver_path)
    try:
        success = client.connect(conn.ip_address, conn.port, conn.timeout)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to connect to CNC")
        client.disconnect()
        return {"status": "success", "message": f"Connected to {conn.ip_address}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/programs/{path_no}")
async def transfer_list_programs(path_no: int, ip_address: str, protocol: str, port: Optional[int] = None, driver_path: Optional[str] = None, file_extensions: Optional[str] = None):
    client = get_client(protocol, driver_path)
    try:
        if not client.connect(ip_address, port):
            raise HTTPException(status_code=500, detail="Failed to connect to CNC")
        extensions = parse_file_extensions(file_extensions)
        programs = client.list_programs(path_no, extensions) if protocol.lower() == "usb" else client.list_programs(path_no)
        return {"status": "success", "programs": programs}
    except TransferError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        client.disconnect()

@router.get("/upload/{path_no}/{prog_num}")
async def transfer_upload(path_no: int, prog_num: int, ip_address: str, protocol: str, port: Optional[int] = None, driver_path: Optional[str] = None, file_extensions: Optional[str] = None):
    client = get_client(protocol, driver_path)
    try:
        if not client.connect(ip_address, port):
            raise HTTPException(status_code=500, detail="Failed to connect to CNC before upload")
        extensions = parse_file_extensions(file_extensions)
        program_text = client.upload_program(prog_num, path_no, extensions) if protocol.lower() == "usb" else client.upload_program(prog_num, path_no)
        print(f"[VSCODE_NOTIFICATION] SUCCESS: Program O{prog_num} successfully pulled from CNC ({ip_address})", flush=True)
        return {"status": "success", "program_text": program_text}
    except TransferError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        client.disconnect()

@router.post("/download/{path_no}")
async def transfer_download(path_no: int, ip_address: str, data: TransferDownloadData):
    client = get_client(data.protocol, data.driver_path)
    try:
        if not client.connect(ip_address, data.port):
            raise HTTPException(status_code=500, detail="Failed to connect to CNC before download")
        client.download_program(data.program_text, path_no, data.file_extension)
        print(f"[VSCODE_NOTIFICATION] SUCCESS: Program successfully pushed to CNC ({ip_address})", flush=True)
        return {"status": "success", "message": "Download to CNC completed successfully"}
    except TransferError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        client.disconnect()
