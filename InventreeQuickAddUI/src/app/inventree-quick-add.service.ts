import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InventreeQuickAddService {

  constructor(private http: HttpClient) {
  }

  public storageLocations(): Observable<any[]> {
    return this.http.get<any[]>(`/api/inventree/storage-locations`);
  }

  public partCategories(): Observable<any[]> {
    return this.http.get<any[]>(`/api/inventree/part-categories`);
  }
}
