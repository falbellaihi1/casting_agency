/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://casting-agency-capstone-udaciy.herokuapp.com/', // the running FLASK api server url
  auth0: {
    url: 'falbellaihi1.us', // the auth0 domain prefix
    audience: 'castingagency', // the audience set for the auth0 app
    clientId: 'pEvos3o5ZG6MTiTSQaT12hDNOEsGJIjR', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:5000', // the base url of the running ionic application.
  }
};
