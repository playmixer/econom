import React from 'react'
import {connect} from "react-redux";
import {
    BrowserRouter,
    Switch,
    Route
} from "react-router-dom";

import Menu from "./components/menu";

import Wallets from './pages/wallets'
import CashFlows from './pages/cashFlows/index'


const Router = ({user}) => {
    return (
        <BrowserRouter>
            {user.isAuth && <Menu/>}
            <Switch>
                <Route path="/wallets" component={Wallets}/>
                <Route path="/expense" component={CashFlows}/>
            </Switch>
        </BrowserRouter>
    )
}

export default connect(state => ({
    user: state.user
}))(Router)
