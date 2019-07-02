import { Component, OnInit } from '@angular/core';
// import {DialogComponent} from '../typography/createofferpopup'
import {  AlertService, AuthenticationService  } from '../services/index'
import {MatDialog} from '@angular/material';
declare var $: any;
@Component({
  selector: 'app-typography',
  templateUrl: './typography.component.html',
  styleUrls: ['./typography.component.css']
})
export class TypographyComponent implements OnInit {
  offers = [];
  currentOffer = {};
  editmode= false;
  popupstatus = false;
  isdisabled = true;
  editstatus = "Edit Offer"
	public movieList =  ['abhiram', 'deadpool' , 'test' ]

  constructor(public dialog:MatDialog, public authenticationService:AuthenticationService) {
    
   }

  ngOnInit() {
    this.currentOffer = {"offer_data":{},"offer_type":"rewardpoints"};
    this.authenticationService.getCurrentOffers("rewardpoints").subscribe(
      data => {
        if(data.error==true){
        console.log(data.message);
        }
        else{
          for(var i in data.offers){
            data.offers[i]['valid_from'] = new Date(data.offers[i]['valid_from'])
            data.offers[i]['valid_to'] = new Date(data.offers[i]['valid_to'])
            data.offers[i]['enabled'] = false;
          }
          this.offers = data.offers;
        }
          
      },
      error => {
        
      });
    
  }
  initcurrentOffers(){
    this.currentOffer = {"offer_data":{},"offer_type":"rewardpoints"};
  }
  validation(offer){
    console.log(offer);
    if(offer["name"]==""){
      return false;
    }
    if(offer["offer_data"]["description"]==""){ return false;}
    if(!("valid_from" in offer)){ return false;}
    if(!("valid_from" in offer)){ return false;}
    return true;
  }
  showNotification(message,notifiationtype){
    const type = ['','info','success','warning','danger'];

    const color = Math.floor((Math.random() * 4) + 1);

    $.notify({
        icon: "notifications",
        message: message

    },{
        type: notifiationtype,
        timer: 1000,
        placement: {
            from: "top",
            align: "right"
        }
    });
}
  
  
  openmodal(){
    $('#offersModal').appendTo("body").modal('show');
    // this.offers = this.authenticationService.getCurrentOffers()['offers'];
    // this.offers.push(this.currentOffer)
  }
  createoffer(){
    this.initcurrentOffers()
    this.popupstatus = true;
    this.openmodal();
  }
  edit(i){
    this.currentOffer = this.offers[i]
    this.currentOffer['currentIndex'] = i
    console.log(this.currentOffer)
    this.openmodal()
    // if(this.editstatus == "Edit Offer"){
    //   this.editstatus = "Cancel"
    //   for(var i in this.offers){
    //     this.offers[i]['edit'] = true
    //   }
    // }
    // else{
    //   this.editstatus = "Edit Offer"
    //   for(var i in this.offers){
    //     this.offers[i]['edit'] = false
    //   }
    // }
  }
  submit(){

    console.log(this.offers);
    console.log(this.currentOffer)
    // this.offers.reverse();
    if("currentIndex" in this.currentOffer){
    this.authenticationService.updateOffer(this.currentOffer,this.currentOffer['_id']).subscribe(
      data => {
        if(data.error==true){
        console.log(data.message);
        }
        else{
          this.showNotification("Offer Successfully Updated","success")
          
          
          data['valid_from'] = new Date(data['valid_from'])
            data['valid_to'] = new Date(data['valid_to'])
            data['enabled'] = false;
          this.offers[this.currentOffer['currentIndex']] = data
          this.initcurrentOffers()
          // this.edit();
        }
          
      },
      error => {
        
      });
    }
      else{this.authenticationService.createOffer(this.currentOffer).subscribe(
        data => {
          if(data.error==true){
          console.log(data.message);
          }
          else{
            this.showNotification("Offer Successfully Created","success")
            this.currentOffer['edit'] = false;
            this.initcurrentOffers()
            data['valid_from'] = new Date(data['valid_from'])
              data['valid_to'] = new Date(data['valid_to'])
              data['enabled'] = false;
            // this.offers.append(data);
            this.offers.splice(0,0,data)
            // this.edit();
          }
            
        },
        error => {
          
        });
      }
    // this.offers.push(this.currentOffer)
    // this.offers.reverse();
    
    // this.currentOffer = {};
    // this.offer['name'] = name;
    // this.offer['description'] = description;
    // this.offer['value'] = value;
    $('#offersModal').modal('hide');

  }

  delete(){
    // const index = this.offers.indexOf(i);
    let i = this.currentOffer['currentIndex']
    let valid = this.validation(this.offers[i])
    console.log(valid)
    if(valid==false){
      this.offers.splice(i, 1); 
      this.initcurrentOffers()
      return false;

    }
    console.log(this.offers[i]);

    this.authenticationService.deleteOffer(this.offers[i]['_id']).subscribe(
      data => { 
        this.showNotification("Offer Deleted","danger")
        this.offers.splice(i, 1); 
        // this.edit();
      },
      error => {});
    
    // this.offers.splice(index, 1);
    // this.offers.reverse();
    // this.offers.pop();
    // this.offers.reverse();
    this.initcurrentOffers()
    $('#offersModal').modal('hide');
  }
}
