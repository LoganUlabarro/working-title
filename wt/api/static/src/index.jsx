import React from 'react';
import ReactDom from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Redirect, browserHistory } from 'react-router';
import injectTapEventPlugin from 'react-tap-event-plugin';

import configureStore from './store/configure';
import routes from './routes';

injectTapEventPlugin();
const store = configureStore();
const history = syncHistoryWithStore(browserHistory, store);

ReactDom.render(
    <Provider store={store}>
        <Router history={history}>
            <Redirect from='/' to='main' />
            {routes}
        </Router>
    </Provider>,
    document.getElementById('wtuiroot')
);
