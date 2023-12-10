import { Injectable } from '@angular/core';
import { MessageService } from 'primeng/api';
import { ToastConfig } from './toast-config';

@Injectable({
  providedIn: 'root'
})
export class ToastHandlerService {
  CONFIG = "lqs_ui/src/app/toastHandle/pop-message-config.json"

  constructor(private messageService: MessageService) {}

  handleToast(data: any){
    if (data.status == 200){
      this.showToast(ToastConfig.S200.severity, ToastConfig.S200.summary, data.message);
    }
    if (data.status == 400){
      this.showToast(ToastConfig.S400.severity, ToastConfig.S400.summary, data.error.detail);
    }
    if (data.status == 404){
      this.showToast(ToastConfig.S404.severity, ToastConfig.S404.summary, ToastConfig.S404.detail);
    }
    if (data.status == 500){
      this.showToast(ToastConfig.S500.severity, ToastConfig.S500.summary, ToastConfig.S500.detail);
    }
  }

  showToast(severity: any, summary: any, detail: any) {
    this.messageService.add({
      severity: severity,
      summary: summary,
      detail: detail,
    });
  }
}
