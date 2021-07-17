import React, {useEffect} from 'react';
import {connect} from "react-redux";
import {source} from './store/actions/user'

import Layout from "./components/layout";
import Auth from "./pages/auth";

import Router from "./router"

import '../src/utils/prototype'

const Index = ({user, dispatch}) => {

    useEffect(() => {
        dispatch(source())
    }, [])


    return (
        <Layout>
            {!user.isAuth && <Auth/>}
            {user.isAuth && <Router/>}
        </Layout>
    );
}

export default connect((state) => ({
    user: state.user
}))(Index)
