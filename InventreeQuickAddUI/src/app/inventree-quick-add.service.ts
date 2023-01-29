import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AddPartParameters } from './add-part-parameters';
import { AutocompleteResult } from './autocomplete-result';

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

  public addPart(part: AddPartParameters): Observable<any> {
    return this.http.post<any>(`/api/inventree/add-part`, part);
  }

  public autocompleteMPN(mpnPart: string): Observable<AutocompleteResult[]> {
    return this.http.get<AutocompleteResult[]>(`/api/search/autocomplete`, {params: {query: mpnPart}});
  }
}
