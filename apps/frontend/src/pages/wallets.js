import React, {useEffect} from 'react'
import {getWallets} from "../store/actions/econom";
import {connect} from "react-redux";


const Wallets = ({econom, dispatch}) => {

    useEffect(() => {
        dispatch(getWallets())
    }, [])

    return (
        <div>
            <h3 className="mb-5">Счета</h3>

            <table className="table table-hover">
                <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Счет</th>
                    <th scope="col">Баланс</th>
                </tr>
                </thead>
                <tbody>
                {Object.keys(econom.wallets).map((key, i) => {
                    return (
                        <tr key={i}>
                            <th scope="row">{i + 1}</th>
                            <td>{econom.wallets[key].title}</td>
                            <td>{econom.wallets[key].balance}</td>
                        </tr>
                    )
                })}
                </tbody>
            </table>
        </div>
    )
}

export default connect(state => ({
    econom: state.econom
}))(Wallets)
