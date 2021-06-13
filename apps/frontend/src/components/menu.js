import React from 'react'
import {connect} from "react-redux"
import {Link} from "react-router-dom"

import {logout} from "../store/actions/user"

const Menu = ({user, dispatch}) => {

    const onLogout = () => {
        dispatch(logout())
    }

    return <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div className="container-fluid">
            <Link to="/" className="navbar-brand">Econom</Link>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                    <li className="nav-item">
                        <Link to="/wallets" className="nav-link" aria-current="page">Счета</Link>
                    </li>
                    <li className="nav-item">
                        <Link to="/expense" className="nav-link">Финансы</Link>
                    </li>
                </ul>
                <span style={{marginRight: "5px"}}>
                    <a href="#" className="link-secondary">{user.model?.username}</a>
                </span>
                <a onClick={onLogout} className="btn btn-outline-primary">Выход</a>
            </div>
        </div>
    </nav>
}

export default connect(state => ({
    user: state.user
}))(Menu)
