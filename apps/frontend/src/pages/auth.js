import React from 'react'

import * as userAction from '../store/actions/user'
import {connect} from 'react-redux'

const Auth = ({user, dispatch}) => {

    const onSignIn = (e) => {
        e.preventDefault()
        const {username, password} = e.target

        dispatch(userAction.signIn({username: username.value, password: password.value}))
    }

    return <div className="row" style={{display: 'flex', justifyContent: "center"}}>
        <div className="col-xl-5 col-lg-6">
            <h3 style={{display: 'flex', justifyContent: "center"}}>Авторизация</h3>
            <form onSubmit={onSignIn}>
                <span>{user.error}</span>
                <div className="mb-3">
                    <div>
                        <label className="form-label" htmlFor="username">Username</label>
                        <input type="text" className={"form-control"} id="username" name={"username"}/>
                    </div>
                    <div>
                        <label className="form-label" htmlFor="password">Password</label>
                        <input type="password" className={"form-control"} id="password" name={"password"}/>
                    </div>
                </div>
                <button type="submit" className="btn btn-primary">Войти</button>
            </form>
        </div>
    </div>
}

export default connect(state => ({
    user: state.user
}))(Auth)
