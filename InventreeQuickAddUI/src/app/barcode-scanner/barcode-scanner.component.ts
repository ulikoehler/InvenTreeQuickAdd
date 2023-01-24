import { Component, OnInit } from '@angular/core';

import { BrowserMultiFormatReader, NotFoundException } from '@zxing/library';
import { __makeTemplateObject } from 'tslib';
import { BarcodeValueDecoderService } from '../barcode-value-decoder.service';

//const hints = new Map();
//const formats = [BarcodeFormat.QR_CODE, BarcodeFormat.DATA_MATRIX/*, ...*/];

//hints.set(DecodeHintType.POSSIBLE_FORMATS, formats);

//const luminanceSource = new RGBLuminanceSource(imgByteArray, imgWidth, imgHeight);
//const binaryBitmap = new BinaryBitmap(new HybridBinarizer(luminanceSource));

//reader.decode(binaryBitmap, hints);

@Component({
  selector: 'app-barcode-scanner',
  templateUrl: './barcode-scanner.component.html',
  styleUrls: ['./barcode-scanner.component.less']
})
export class BarcodeScannerComponent implements OnInit {

  codeReader = new BrowserMultiFormatReader();

  noVideoInputDevicesFound = false;

  selectedVideoDevice: string = ''; // deviceId of MediaDeviceInfo
  selectableVideoDevices: MediaDeviceInfo[] = [];

    // If started, we need to stop before starting again
  _started = false;

  result = '';

  constructor(private decoder: BarcodeValueDecoderService) {
  }

  startQRDecoding() {
    if(this.selectedVideoDevice == null) {
      console.error("Called startQRDecoding() without video input device set");
      return;
    }
    // OK, we have some video device

    // Do we need to stop the previous encoding?
    if(this._started) {
      console.info("Stopping previous video source");
      this.codeReader.stopContinuousDecode();
      this.codeReader.stopAsyncDecode();
      this.codeReader.reset();
    }

    this._started = true;
    console.log(this.selectableVideoDevices)
    console.info(`Starting video source`, this.selectedVideoDevice)

    const constraints: MediaStreamConstraints = { video: {
            deviceId: { exact: this.selectedVideoDevice },

        }
    };
    this.codeReader.decodeFromConstraints(constraints, 'video', (result, err) => {
      if (result) {
        console.log(result)
        const decodingResult = this.decoder.decodeBarcode(result);
        console.log(decodingResult);
      }
      if (err && !(err instanceof NotFoundException)) {
        console.error(err)
        //document.getElementById('result').textContent = err
      }
    }).catch(ex => {
      console.error(ex)
    })
  }

  ngOnInit(): void {
    this.codeReader.listVideoInputDevices().then((videoInputDevices: MediaDeviceInfo[]) => {
      console.info(videoInputDevices);
      const numVideoDevices = videoInputDevices.length;
      if(numVideoDevices == 0) {
        console.log("No video device available");
      } else if(numVideoDevices == 1) {
        // Auto-select this one video device
        // Do not display the video device selector
        this.selectedVideoDevice = videoInputDevices[0].deviceId;
        console.log("Selected single video device", this.selectedVideoDevice)
        this.startQRDecoding();
      } else {
        // Multiple devices available
        // Select first one
        // TODO display selecotr
        this.selectableVideoDevices = videoInputDevices;
        this.selectedVideoDevice = videoInputDevices[0].deviceId;
        console.log("Selected first video device", this.selectedVideoDevice)
        this.startQRDecoding();
      }
      /*
      const sourceSelect = document.getElementById('sourceSelect')
      this.selectedDeviceId = videoInputDevices[0].deviceId
      if (videoInputDevices.length >= 1) {
        videoInputDevices.forEach((videoInputDevices) => {
          const sourceOption = document.createElement('option')
          sourceOption.text = element.label
          sourceOption.value = element.deviceId
          sourceSelect.appendChild(sourceOption)
        })

        sourceSelect.onchange = () => {
          selectedDeviceId = sourceSelect.value;
        };

        const sourceSelectPanel = document.getElementById('sourceSelectPanel')
        sourceSelectPanel.style.display = 'block'
      });*/
    });
  }

}
