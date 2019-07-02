import { Component, OnInit } from '@angular/core';
import * as Chartist from 'chartist';
import {  AlertService, AuthenticationService  } from '../services/index'
import { CanColor } from '@angular/material';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  overviewInfo = {};
  weeklyusers = {};
  totalusers = {};
  totalrevenue = {};
  totaltransactions = {};
  weeklytransactions = {};
  usersoverview = {};
  usersbymonth = {};
  transactionsbymonth = {};
  revenuebymonth = {};
  usersrewardpoints = {};
  successfulloffer = {};
  constructor(public authenticationService:AuthenticationService) {  }
  startAnimationForLineChart(chart){
      let seq: any, delays: any, durations: any;
      seq = 0;
      delays = 80;
      durations = 500;

      chart.on('draw', function(data) {
        if(data.type === 'line' || data.type === 'area') {
          data.element.animate({
            d: {
              begin: 600,
              dur: 700,
              from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
              to: data.path.clone().stringify(),
              easing: Chartist.Svg.Easing.easeOutQuint
            }
          });
        } else if(data.type === 'point') {
              seq++;
              data.element.animate({
                opacity: {
                  begin: seq * delays,
                  dur: durations,
                  from: 0,
                  to: 1,
                  easing: 'ease'
                }
              });
          }
      });

      seq = 0;
  };
  startAnimationForBarChart(chart){
      let seq2: any, delays2: any, durations2: any;

      seq2 = 0;
      delays2 = 80;
      durations2 = 500;
      chart.on('draw', function(data) {
        if(data.type === 'bar'){
            seq2++;
            data.element.animate({
              opacity: {
                begin: seq2 * delays2,
                dur: durations2,
                from: 0,
                to: 1,
                easing: 'ease'
              }
            });
        }
      });

      seq2 = 0;
  };
  ngOnInit() {
      /* ----------==========     Daily Sales Chart initialization For Documentation    ==========---------- */
      this.authenticationService.getTotalUsers().subscribe(
        
          data=>{this.totalusers = data;
          console.log(this.totalusers)}
      )
      this.authenticationService.getWeeklyUsers().subscribe(

        data=>{this.weeklyusers = data;
        console.log(this.weeklyusers)}
    )
    this.authenticationService.getTotalRevenue().subscribe(
        
      data=>{this.totalrevenue = data;
      console.log(this.totalrevenue)}
  )
    this.authenticationService.getTotalTransactions().subscribe(
        
    data=>{this.totaltransactions = data;
    console.log(this.totalusers)}
)
    this.authenticationService.getWeeklyTransactions().subscribe(
  
  data=>{this.weeklytransactions = data;
  console.log(this.weeklyusers)}
)
    this.authenticationService.getUsersOverview().subscribe(
  
  data=>{this.usersoverview = data;
  console.log(this.usersoverview)}
)


this.authenticationService.usersGraph().subscribe(
  
  data=>{this.usersbymonth = data;
  console.log(this.usersbymonth)

      const dataDailySalesChart: any = {
          labels: data['months'],
          series: [
              data['values']
          ]
      };

     const optionsDailySalesChart: any = {
          lineSmooth: Chartist.Interpolation.cardinal({
              tension: 0
          }),
          
          low: 0,
          
          high: data['max'], // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: { top: 0, right: 0, bottom: 0, left: 0},
      }

      var dailySalesChart = new Chartist.Line('#dailySalesChart', dataDailySalesChart, optionsDailySalesChart);

      this.startAnimationForLineChart(dailySalesChart);
  })

      /* ----------==========     Completed Tasks Chart initialization    ==========---------- */
      this.authenticationService.revenueGraph().subscribe(
  
        data=>{this.revenuebymonth = data;
        console.log(this.revenuebymonth)

      const dataCompletedTasksChart: any = {
          labels: data["months"],
          series: [
              data["values"]
          ]
      };

     const optionsCompletedTasksChart: any = {
          lineSmooth: Chartist.Interpolation.cardinal({
              tension: 0
          }),
          low: 0,
          high: data['max'], // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: { top: 0, right: 0, bottom: 0, left: 0}
      }

      var completedTasksChart = new Chartist.Line('#completedTasksChart', dataCompletedTasksChart, optionsCompletedTasksChart);

      // start animation for the Completed Tasks Chart - Line Chart
      this.startAnimationForLineChart(completedTasksChart);
      }
      )


      /* ----------==========     Emails Subscription Chart initialization    ==========---------- */
      this.authenticationService.transactionsGraph().subscribe(
  
        data=>{this.transactionsbymonth = data;
        console.log(this.transactionsbymonth)
      var dataEmailsSubscriptionChart = {
        labels: data["months"],
        series: [
          data['values']

        ]
      };
      var optionsEmailsSubscriptionChart = {
          axisX: {
              showGrid: false
          },
          low: 0,
          high: data['max'],
          chartPadding: { top: 0, right: 5, bottom: 0, left: 0}
      };
      var responsiveOptions: any[] = [
        ['screen and (max-width: 640px)', {
          seriesBarDistance: 5,
          axisX: {
            labelInterpolationFnc: function (value) {
              return value[0];
            }
          }
        }]
      ];
      var emailsSubscriptionChart = new Chartist.Bar('#emailsSubscriptionChart', dataEmailsSubscriptionChart, optionsEmailsSubscriptionChart, responsiveOptions);

      //start animation for the Emails Subscription Chart
      this.startAnimationForBarChart(emailsSubscriptionChart);
    }
  )
  this.authenticationService.successfullOffer().subscribe(
  
    data=>{this.successfulloffer = data;
    console.log(this.successfulloffer)

  })
  this.authenticationService.UsersHoldingRewardPoints().subscribe(
  
    data=>{this.usersrewardpoints = data;
    console.log(this.usersrewardpoints)

  })
}

}
