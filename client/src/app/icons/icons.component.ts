import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material';
import {  AlertService, AuthenticationService  } from '../services/index'
import { FileUploader,FileUploaderOptions } from 'ng2-file-upload';
const URL = 'http://192.168.1.102:5000/agent';
declare var $: any;
@Component({
  selector: 'app-icons',
  templateUrl: './icons.component.html',
  styleUrls: ['./icons.component.css']
})

export class IconsComponent implements OnInit {
  
showDialog = false;
private fileText;
agentData = {};
imagedata :"";
backgroundimgs = ["https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?auto=compress&cs=tinysrgb&h=350","https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg","https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?auto=compress&cs=tinysrgb&h=350","https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg"];
filecontent:any;
currentimg="";
currentimgcount = 0;
starttime = "01:22 AM";
uploader:FileUploader = new FileUploader({url:URL});
uploaderOptions: FileUploaderOptions = {};
  constructor(public authenticationService:AuthenticationService, public matDialog:MatDialog) { 
    this.authenticationService.getBackgroundImages().subscribe(
      data=>{this.backgroundimgs  = data['imgs']  
    })
  }

  ngOnInit() {
    this.agentData = JSON.parse(localStorage.getItem("agentData"));
    console.log(this.agentData['starttime']);
    this.currentimgcount = 0;
    
    // this.starttime = data['starttime'];
    // this.endtime = data['endtime'];
  }
  showNotification(from, align,notifiationtype){
    const type = ['','info','success','warning','danger'];

    const color = Math.floor((Math.random() * 4) + 1);

    $.notify({
        icon: "notifications",
        message: "Profile Successfully Updated"

    },{
        type: type[notifiationtype],
        timer: 1000,
        placement: {
            from: from,
            align: align
        }
    });
}

  updateAgentProfile(){
  // console.log(this.starttime);
  // console.log(this.agentData);
  
  // this.uploaderOptions['url'] = URL;
  // this.uploaderOptions['method'] = 'GET';
  // this.uploaderOptions['headers'] = [{ name: 'auth-token', value : this.agentData['auth-token'] },{ name: 'token', value : this.agentData['token'] } ];
  // this.uploaderOptions['autoUpload'] = false;
  // this.uploader.setOptions(this.uploaderOptions);
  // console.log(this.uploader.queue[0].formData);
  console.log("sdfsad");
  var content
  let reader = new FileReader();
  var self = this
  let agentData = this.agentData
  try{
  reader.readAsDataURL(this.filecontent);
      reader.onload = function () {
        const formData: FormData = new FormData();
        content = reader.result
        formData.append('myfile', content)
        // imgcontent = formData
        // updateglobal(formData)
        // return formData
        console.log(agentData);
        self.authenticationService.updateProfilefile(formData,agentData['auth-token'],agentData['token']).subscribe(
  
          data=>{self.agentData  = data
            self.filecontent = '';
      
        })
        
      }
    }
    catch(e){
      
    }
      this.authenticationService.updateProfile(this.agentData).subscribe(
  
        data=>{this.agentData  = data
          console.log(this.agentData)
    
      })
      

  //     var i =1;
  //     function myLoop () {           //  create a loop function
  //       setTimeout(function () {    //  call a 3s setTimeout when the loop is called
  //          console.log("123");       //  your code here
  //          i++;       
  //          if(i==2){
  //            console.log('ff');
  //          }
  //         //  this.agentData['updated_at']              //  increment the counter
  //         //  JSON.parse(localStorage.getItem("agentData"))['updated_at']
  //         //  while (this.agentData['updated_at']==JSON.parse(localStorage.getItem("agentData"))['updated_at']) {            //  if the counter < 10, call the loop function
  //         //     myLoop();             //  ..  again which will trigger another 
  //         //  }                        //  ..  setTimeout()
  //       }, 1000)
  //    }
     
     
  // while(agentData['updated_at']==JSON.parse(localStorage.getItem("agentData"))['updated_at']){
  //   console.log("asdf");
  //   myLoop()
  // }
  // this.agentData =this.authenticationService.updateProfile(this.agentData)
  
  // console.log(this.uploader.queue[0].formData);
  this.showNotification("top","right",2);
}
  uploadFile(event){
    const formData: FormData = new FormData();
    // console.log(this.uploader);
    // this.uploader.queue[0].upload();
  // console.log(this.filepath);
  console.log(event);
  let files = event.target.files;
  console.log(event.target)
  for (let i = 0; i < files.length; i++) {
    formData.append('file', files[i]);
  }
  console.log(formData);
  // console.log(files);
  // if (files.length > 0) {
  //   console.log(files); // You will see the file
    //this.service.uploadFile(file);
  // }
  }
  openmodal(){
    $('#offersModal').appendTo("body").modal('show');
    this.currentimg = this.backgroundimgs[0]
    // this.offers = this.authenticationService.getCurrentOffers()['offers'];
    // this.offers.push(this.currentOffer)
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
    this.agentData['primary_image'] = this.currentimg;
  }
  updateglobal(formData){
    console.log(formData)
    this.imagedata = formData;
  }
  onFileChange(event){
    console.log("dfasd");
    var content
    var imgcontent
    let reader = new FileReader();
    if(event.target.files && event.target.files.length > 0) {
      console.log();
      let file = event.target.files[0];
      let authenticationService = this.authenticationService
      let updateglobal = this.updateglobal
      let agentData = this.agentData
      reader.readAsDataURL(file);
      this.filecontent = file;
      reader.onload = function () {
        const formData: FormData = new FormData();
        content = reader.result
        formData.append('myfile', content)
        // imgcontent = formData
        // updateglobal(formData)
        // return formData
        // authenticationService.updateProfilefile(formData,agentData['auth-token'],agentData['token'])
      }
      // this.imagedata = imgcontent
      
      
    }
  }

}
