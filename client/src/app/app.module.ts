import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';
import { MdButtonModule } from '@angular2-material/button';
import { MatInputModule, MatButtonModule} from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatNativeDateModule} from '@angular/material';
import { MatCheckboxModule } from '@angular/material';
import {MatDatepickerModule} from '@angular/material';
import { AuthenticationService, AlertService } from './services/index';
import {MatSelectModule , MatOptionModule} from '@angular/material';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthGuard } from './auth_guard'
import { AppRoutingModule } from './app.routing';
import { ComponentsModule } from './components/components.module';
import { FileSelectDirective } from 'ng2-file-upload';
import { AppComponent } from './app.component';
import  { LoginComponent } from './login.component';
import  { HomepageComponent } from './homepage.component';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { DashboardComponent } from './dashboard/dashboard.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { TableListComponent } from './table-list/table-list.component';
import { TypographyComponent } from './typography/typography.component';

import { IconsComponent } from './icons/icons.component';
import { DialogComponent } from './icons/dialog.component';
import { MapsComponent } from './maps/maps.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { UpgradeComponent } from './upgrade/upgrade.component';
import { DateAdapter, NativeDateAdapter } from '@angular/material';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomepageComponent,
    DashboardComponent,
    UserProfileComponent,
    TableListComponent,
    TypographyComponent,
    IconsComponent,
    MapsComponent,
    NotificationsComponent,
    UpgradeComponent,
    DialogComponent,
    FileSelectDirective
    

  ],
  imports: [
    MatNativeDateModule,
    MatDatepickerModule,
    MatButtonModule,
    MatCheckboxModule,
    MatSlideToggleModule,
    MatSelectModule,
    MatOptionModule,
    BrowserAnimationsModule,
    MdButtonModule,
    MatInputModule,
    BrowserModule,
    FormsModule,
    HttpModule,
    HttpClientModule,
    ComponentsModule,
RouterModule,
    AppRoutingModule
  ],
  providers: [AuthenticationService,AlertService,AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
