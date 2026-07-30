import { TransferProgram } from '@core/types';
import { BackendGateway } from '../BackendGateway';
import { ITransferProtocol } from './ITransferProtocol';

export class UsbTransferProtocol implements ITransferProtocol {
  constructor(private backend: BackendGateway) {}

  async ping(rootPath: string): Promise<boolean> {
    const res = await this.backend.transferPing(rootPath, 'usb');
    return res.available;
  }

  async connect(rootPath: string): Promise<void> {
    await this.backend.transferConnect(rootPath, 0, 'usb');
  }

  async listPrograms(rootPath: string, pathNo: number, _port?: number, fileExtensions?: string[]): Promise<TransferProgram[]> {
    const res = await this.backend.transferListPrograms(rootPath, pathNo, 0, 'usb', undefined, fileExtensions);
    return res.programs || [];
  }

  async uploadProgram(rootPath: string, pathNo: number, progNum: number, _port?: number, fileExtensions?: string[]): Promise<string> {
    const res = await this.backend.transferUpload(rootPath, pathNo, progNum, 0, 'usb', undefined, fileExtensions);
    return res.program_text;
  }

  async downloadProgram(rootPath: string, pathNo: number, programText: string, _port?: number, fileExtension?: string): Promise<void> {
    await this.backend.transferDownload(rootPath, pathNo, programText, 0, 'usb', undefined, fileExtension);
  }
}