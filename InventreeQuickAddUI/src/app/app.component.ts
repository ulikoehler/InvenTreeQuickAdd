import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {

  text: string = "a";

  results: string[] = ["a", "b", "c", "d"];

  search(event: any) {
  }

}
