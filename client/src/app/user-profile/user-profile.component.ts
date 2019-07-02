import { Component, OnInit } from '@angular/core';
import { DateAdapter, NativeDateAdapter } from '@angular/material';
import {  AlertService, AuthenticationService  } from '../services/index'
import {MatDialog} from '@angular/material';

declare var $: any;
@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  offers = [];
  currentOffer = {};
  editmode= false;
  popupstatus = false;
  promotionenabled = true;
  isdisabled = true;
  promotiontype="";
  backgroundimgs = ["https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?auto=compress&cs=tinysrgb&h=350","https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg","https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?auto=compress&cs=tinysrgb&h=350","https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg"];
filecontent:any;
currentimg="";
currentimgcount = 0;
  send_at_list = [
    {value: '08:00', viewValue: 'Noon (8 AM)'},
    {value: '12:00', viewValue: 'Noon (12 PM)'},
    {value: '16:00', viewValue: 'Evening (4 PM)'},
    {value: '19:00', viewValue: 'Night (7 PM)'}
    
  ];
  
  promotion_category = [
    {value: "offer", viewValue: 'Offer Campaign'},
    {value: "birthday", viewValue: 'Birthday Campaign'},
    {value: "scheduler", viewValue: 'Scheduled Campaign'}
    
  ];
  sendtolist = [
    {value: 'all', viewValue: 'All Customers'},
    {value: 'visited', viewValue: 'Your Customers'},
    {value: 'birthday', viewValue: 'Birthday'}
    
  ];
  constructor(dateAdapter: DateAdapter<NativeDateAdapter>,public dialog:MatDialog, public authenticationService:AuthenticationService) {
    dateAdapter.setLocale('en');
    this.authenticationService.getBackgroundImages().subscribe(
      data=>{this.backgroundimgs  = data['imgs']  
    })
  }

  ngOnInit() {
    this.currentimgcount = 0;
    this.currentOffer = {"promotion_data":{"promotionenabled":false,"birthdayenabled":false},"offer_type":"promotions"};
    this.authenticationService.getCurrentOffers("promotions").subscribe(
      data => {
        if(data.error==true){
        console.log(data.message);
        }
        else{
          for(var i in data.offers){
            data.offers[i]['valid_from'] = new Date(data.offers[i]['valid_from'])
            data.offers[i]['valid_to'] = new Date(data.offers[i]['valid_to'])
            data.offers[i]['scheduled_at'] = new Date(data.offers[i]['scheduled_at'])
            data.offers[i]['enabled'] = false;
          }
          this.offers = data.offers;
        }
          
      },
      error => {
        
      });
    
  }
  initcurrentOffers(){
    this.currentOffer = {"promotion_data":{"promotionenabled":false,"birthdayenabled":false,"schedulerenabled":false},"offer_type":"promotions"};
  }
  objChanged(event){
    if(this.promotiontype=="birthday"){
      this.currentOffer['promotion_data']['promotionenabled']=false;
      this.currentOffer['promotion_data']['birthdayenabled']=true;
      this.currentOffer['promotion_data']['schedulerenabled']=false;
      this.currentOffer['promotion_data']['sendto']="visited";
    }
    else if(this.promotiontype=="offer"){
      this.currentOffer['promotion_data']['promotionenabled']=false;
      this.currentOffer['promotion_data']['birthdayenabled']=false;
      this.currentOffer['promotion_data']['schedulerenabled']=false;
    }
    else if(this.promotiontype=="scheduler"){
      this.currentOffer['promotion_data']['promotionenabled']=false;
      this.currentOffer['promotion_data']['birthdayenabled']=false;
      this.currentOffer['promotion_data']['schedulerenabled']=true;
      this.currentOffer['promotion_data']['sendto']="visited";
    }
    console.log(event)
    console.log(JSON.stringify(this.currentOffer));
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
    const sendtolist = [
      {value: 'steak-0', viewValue: 'Steak'},
      {value: 'pizza-1', viewValue: 'Pizza'},
      {value: 'tacos-2', viewValue: 'Tacos'}
    ];
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
    $('#PromotionsModal').appendTo("body").modal('show');
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
    console.log(this.currentOffer)
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
            data['scheduled_at'] = new Date(data['scheduled_at'])
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
              data['scheduled_at'] = new Date(data['scheduled_at'])
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
    $('#PromotionsModal').modal('hide');

  }
  selectimage(){
    $('#selectbackgroundimageModel').appendTo("body").modal('show');
    this.currentimg = this.backgroundimgs[0]
  }
  nextImg(){
    this.currentimgcount = this.currentimgcount +1;
    this.currentimg = this.backgroundimgs[this.currentimgcount]
  }
  prevImg(){
    this.currentimgcount = this.currentimgcount - 1;
    this.currentimg = this.backgroundimgs[this.currentimgcount]
  }
  Select(){
    this.currentimgcount = 0;
    this.currentOffer["promotion_data"]['background_image'] = this.currentimg;
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
    $('#PromotionsModal').modal('hide');
  }

}
