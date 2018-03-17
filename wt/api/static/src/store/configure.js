import { createStore, applyMiddleware } from 'redux';
import rootReducer from '../reducers';

export default function configureStore(initialstate) {
    const store = createStore(
        rootReducer,
        initialstate
    );

    if (module.hot) {
        // enables webpack hot reload
        module.hot.accept('../reducers', () => {
            const nextRootReducer = require('../reducers/index').default;
            store.replaceReducer(nextRootReducer);
        });
    }

    return store;
}
