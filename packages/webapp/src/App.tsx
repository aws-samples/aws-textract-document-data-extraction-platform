// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import './App.css';

import { AmplifyAuthenticator, AmplifySignIn } from '@aws-amplify/ui-react';
import { Auth } from 'aws-amplify';
import {
  AppLayout,
  BreadcrumbGroup,
  ButtonDropdown,
  Header,
  Inline,
  NorthStarThemeProvider,
  NotificationButton,
  SideNavigation,
} from 'aws-northstar';
import { SideNavigationItemType } from 'aws-northstar/components/SideNavigation';
import { useState } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Dashboard from './components/dashboard';
import { Document } from './components/document';
import DocumentSchemas from './components/document-schemas';
import PDFFormReview from './components/review';

const App: React.FC = () => {
  const [user, setUser] = useState<any>();

  return (
    <AmplifyAuthenticator
      handleAuthStateChange={async () => {
        try {
          setUser(await Auth.currentAuthenticatedUser());
        } catch (err) {
          setUser(undefined);
        }
      }}
    >
      <AmplifySignIn slot="sign-in">
        <div slot="secondary-footer-content"/>
        <div slot="federated-buttons"/>
      </AmplifySignIn>
      {user ? (
        <NorthStarThemeProvider>
          <BrowserRouter>
            <AppLayout
              header={
                <Header
                  title="Document Data Extraction Platform"
                  rightContent={
                    <Inline>
                      <NotificationButton onDismissNotification={console.log} />
                      <ButtonDropdown
                        darkTheme
                        content={`Hello, ${user?.attributes?.given_name || user?.username}`}
                        items={[
                          {
                            text: 'Sign Out',
                            onClick: async () => {
                              await Auth.signOut();
                              window.location.reload();
                            },
                          },
                        ]}
                      />
                    </Inline>
                  }
                />
              }
              breadcrumbs={
                <BreadcrumbGroup
                  availableRoutes={[
                    { path: '/', exact: true, strict: true },
                    { path: '/docs', exact: true, strict: true },
                    { path: '/review/:documentId/:formId', exact: true, strict: true },
                    { path: '/view/:documentId', exact: true, strict: true },
                    { path: '/view/:documentId/:formId', exact: true, strict: true },
                    { path: '/users', exact: true, strict: true },
                    { path: '/admin', exact: true, strict: true },
                  ]}
                />
              }
              navigation={
                <SideNavigation
                  header={{
                    href: '/',
                    text: 'Dashboard',
                  }}
                  items={[
                    {
                      type: SideNavigationItemType.LINK,
                      text: 'Document Schemas',
                      href: '/docs',
                    },
                    {
                      type: SideNavigationItemType.LINK,
                      text: 'Admin',
                      href: '/admin',
                    },
                    {
                      type: SideNavigationItemType.LINK,
                      text: 'API Documentation',
                      href: '/api-docs/index.html',
                    },
                  ]}
                >
                </SideNavigation>
              }
            >
              <Switch>
                <Route
                  exact
                  path="/"
                  component={() => <Dashboard />}
                  key={'dashboard'}
                />
                <Route
                  exact
                  path="/docs"
                  component={() => <DocumentSchemas />}
                  key={'docs'}
                />
                <Route
                  exact
                  path='/review/:documentId/:formId'
                  component={() => <PDFFormReview isReadOnly={false}/>}
                  key={'review'}
                />
                <Route
                  exact
                  path='/view/:documentId/:formId'
                  component={() => <PDFFormReview isReadOnly={true}/>}
                  key={'view'}
                />
                <Route
                  exact
                  path='/view/:documentId'
                  component={() => <Document/>}
                  key={'viewDocument'}
                />
                <Route
                  exact
                  path="/admin"
                  component={() => <>other admin options</> }
                  key={'admin'}
                />
              </Switch>
            </AppLayout>
          </BrowserRouter>
        </NorthStarThemeProvider>
      ) : (
        <></>
      )}
    </AmplifyAuthenticator>
  );
};

export default App;


