import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      { path: '#/user-page', loadChildren: '../user-page/user-page.module#UserPagePageModule' },
      {
        path: '#/user-page',
        redirectTo: '/tabs/user-page',
        pathMatch: 'full',
        loadChildren: '../user-page/user-page.module#UserPagePageModule'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/user-page',
    pathMatch: 'full',
    loadChildren: '../user-page/user-page.module#UserPagePageModule'
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}
