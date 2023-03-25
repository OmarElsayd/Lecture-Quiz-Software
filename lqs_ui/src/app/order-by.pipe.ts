import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'orderBy',
})
export class OrderByPipe implements PipeTransform {
  transform(value: any[], propertyName: string): any[] {
    return value.slice().sort((a, b) => a[propertyName] - b[propertyName]);
  }
}