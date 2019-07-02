import { NgModule } from '@angular/core';
import { CommonModule, } from '@angular/common';
import { BrowserModule  } from '@angular/platform-browser';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './auth_guard'
import  { LoginComponent } from './login.component';
import  { HomepageComponent } from './homepage.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { TableListComponent } from './table-list/table-list.component';
import { TypographyComponent } from './typography/typography.component';
import { IconsComponent } from './icons/icons.component';
import { MapsComponent } from './maps/maps.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { UpgradeComponent } from './upgrade/upgrade.component';

const routes: Routes =[
    {path: '', redirectTo: 'login', pathMatch: 'full'},
    {path: 'login', component: LoginComponent},
    {path: 'homepage', component: HomepageComponent,
      children:[
        { path: 'dashboard',      component: DashboardComponent ,canActivate: [AuthGuard] },
        { path: 'campaign',   component: UserProfileComponent ,canActivate: [AuthGuard] },
        { path: 'feedback',     component: TableListComponent ,canActivate: [AuthGuard] },
        { path: 'rewards',     component: TypographyComponent ,canActivate: [AuthGuard]},
        { path: 'profile',          component: IconsComponent ,canActivate: [AuthGuard] },
        //{ path: 'maps',           component: MapsComponent },
        { path: 'notifications',  component: NotificationsComponent ,canActivate: [AuthGuard] },
        { path: 'upgrade',        component: UpgradeComponent ,canActivate: [AuthGuard]},
        { path: '',          redirectTo: 'dashboard', pathMatch: 'full' }
      ]
    }
];

@NgModule({
  imports: [
    CommonModule,
    BrowserModule,
    RouterModule.forRoot(routes)
  ],
  exports: [
  ],
})
export class AppRoutingModule { }
import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

