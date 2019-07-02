import { Component, OnInit } from '@angular/core';
import {  AlertService, AuthenticationService  } from '../services/index'


@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.css']
})
export class TableListComponent implements OnInit {
  skip = 0
  limit = 10
  count = 0
  feedbackdata = [{"consumerId":"1231231","message":"Hello How are you","value":5},{"consumerId":"1231231","message":"Hello How are you","value":5},{"consumerId":"1231231","message":"Hello How are you","value":5},{"consumerId":"1231231","message":"Hello How are you","value":5},{"consumerId":"1231231","message":"Hello How are you","value":5}]
  constructor(public authenticationService:AuthenticationService) { }

  ngOnInit() {
    this.authenticationService.getFeedback(this.skip.toString(),this.limit.toString()).subscribe(
  
      data=>{this.feedbackdata  = data['feedback']
        if(this.feedbackdata.length==10){
          this.count=1
        }
        console.log(this.feedbackdata)
  
    })
    
  }
  next(){
    this.skip = this.limit
    this.ngOnInit()
  }

  previous(){
    this.skip = this.skip-10
    this.ngOnInit()
  }
}
