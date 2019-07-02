import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
 
@Injectable()
export class AuthenticationService {
    API_URL="http://localhost:3000/";
    constructor(private http: HttpClient) { }
 
    login(username: string, password: string) {
    const  headers = new HttpHeaders({"api-key":"9MSkGq32VLjzs2Sv"});

     
        return this.http.post<any>(this.API_URL+'login/agent', {"email":username,"password":password}, {headers:headers})
            .map(user => {
                // login successful if there's a jwt token in the response
                    if(user.error!=true){localStorage.setItem('agentData', JSON.stringify(user));}
                    // store user details and jwt token in local storage to keep user logged in between page refreshes
                    
                return user;
            });
    }
    updateProfile(content:object){
        const  headers = new HttpHeaders({"api-key":"9MSkGq32VLjzs2Sv","auth-token":content['auth-token'],"token":content["token"]});

         
            return this.http.put(this.API_URL+'agent', content, {headers:headers})
                .map(user => {
                    // login successful if there's a jwt token in the response
                        if(user["error"]!=true){
                            let oldagentdata = JSON.parse(localStorage.getItem("agentData"));
                            user['token'] = oldagentdata['token']
                            user['auth-token'] = oldagentdata['auth-token']
                            localStorage.setItem('agentData', JSON.stringify(user));}
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return user;
                });

    } 
    updateProfilefile(content:object,auth_token:string,token:string){
        // var gg:any;
        const  headers = new HttpHeaders({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','auth-token':auth_token,'token':token});

         
            return this.http.put(this.API_URL+'backgroundimg/agent', content, {headers:headers})
                .map(user => {
                    // login successful if there's a jwt token in the response
                        if(user["error"]!=true){
                            let oldagentdata = JSON.parse(localStorage.getItem("agentData"));
                            user['token'] = oldagentdata['token']
                            user['auth-token'] = oldagentdata['auth-token']
                            localStorage.setItem('agentData', JSON.stringify(user));
                        }
                  
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return user;
                });

    } 
    getBackgroundImages(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token']
            })
          };

            return this.http.get<any>(this.API_URL+"backgroundimgs", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
                
    }
    getCurrentOffers(offer_type){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true",
              "offer_type":offer_type
            })
          };

            return this.http.get<any>(this.API_URL+"offers", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
                
    }
    createOffer(content){
        console.log("inside");
        
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        console.log(agentData)
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token']
            
            })
          };

            return this.http.post<any>(this.API_URL+"offers",content, httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
                
    }
    deleteOffer(id){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };

            return this.http.delete<any>(this.API_URL+"offers/"+id, httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    updateOffer(content,id){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };

            return this.http.put<any>(this.API_URL+"offers/"+id,content, httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    getCurrentPromotions(offer_type){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true",
              "offer_type":offer_type
            })
          };

            return this.http.get<any>(this.API_URL+"promotion_schedulers", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
                
    }
    createPromotion(content){
        console.log("inside");
        
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        console.log(agentData)
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token']
            
            })
          };

            return this.http.post<any>(this.API_URL+"promotion_schedulers",content, httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
                
    }
    deletePromotion(id){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };

            return this.http.delete<any>(this.API_URL+"promotion_schedulers/"+id, httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    updatePromotion(content,id){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };

            return this.http.put<any>(this.API_URL+"promotion_schedulers/"+id,content, httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }

    getFeedback(skip,limit){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'skip':skip,'limit':limit
            })
          };
          return this.http.get<any>(this.API_URL+"feedback", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });

    }

    getUsersOverview(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/overviewusers", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    getTotalUsers(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/totalusers", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    getWeeklyUsers(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/weeklyusers", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    getTotalRevenue(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/totalrevenue", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }

    getTotalTransactions(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/totaltransactions", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    getWeeklyTransactions(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/weeklytransactions", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    usersGraph(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/users", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    revenueGraph(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/revenue", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    transactionsGraph(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/transactions", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    successfullOffer(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/successfulloffer", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    UsersHoldingRewardPoints(){
        var agentData = JSON.parse(localStorage.getItem('agentData'));
        const httpOptions = {
            headers: new HttpHeaders({
              'auth-token':agentData['auth-token'],
              'token':agentData['token'],
              'present':"true"
            })
          };
          return this.http.get<any>(this.API_URL+"analytics/userrewardpoints", httpOptions)
                .map(res => {
                    console.log(res);
                    // login successful if there's a jwt token in the response
                        // store user details and jwt token in local storage to keep user logged in between page refreshes
                        
                    return res;
                },
            error => {
                console.log(error);
            });
    }
    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('agentData');
    }
}