import React from 'react';
import {render} from "react-dom";
import { Provider} from "react-redux";
import store from './store/store'
import Modal from "react-modal"

import Index from './index'


const App = () => {

    return (
        <Provider store={store}>
            <Index/>
        </Provider>
    );
}

export default App

const container = document.getElementById("app")
render(<App/>, container)

Modal.setAppElement(container)
