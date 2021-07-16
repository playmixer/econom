import React from 'react'
import {connect} from "react-redux";
import {
    BrowserRouter,
    Switch,
    Route
} from "react-router-dom";

import config from "../../../config.json"

import Menu from "./components/menu";

import Wallets from './pages/wallets'
import CashFlows from './pages/cashFlows/index'

const link = (url) => {
    return `${config.subdirectory}/${url}`
}

const routes = [
    {
        path: link("/"),
        component: Wallets
    },
    {
        path: link("wallets"),
        component: Wallets
    },
    {
        path: link("expense"),
        component: CashFlows
    },
]

const Router = ({user}) => {
    console.log(routes)
    return (
        <BrowserRouter>
            {user.isAuth && <Menu/>}
            <Switch>
                {routes.map((v, i) =>
                    <Route key={i} path={v.path} component={v.component}/>
                )}
            </Switch>
        </BrowserRouter>
    )
}

export default connect(state => ({
    user: state.user
}))(Router)
