import React, {useEffect} from "react";
import * as actionEconom from "../../store/actions/econom";
import {connect} from "react-redux";
import {sortDate} from "../../utils/sort";


const Expense = ({econom, dispatch, period, local}) => {

    useEffect(() => {
        dispatch(actionEconom.getWallets())
        dispatch(actionEconom.getExpense({month:period.month, year: period.year}))
    }, [period])

    return (
        <div>
            <h1>{local.title}</h1>
            <div className="mb-2">
                <a href="{{ url_for('.income_add') }}" className="btn btn-outline-primary">Внести расходы</a>
            </div>
            <table className="table table-hover">
                <thead>
                <tr>
                    <th width="15">{local.table[0]}</th>
                    <th width="200">{local.table[1]}</th>
                    <th>{local.table[2]}</th>
                    <th width="100">{local.table[3]}</th>
                    <th width="120">{local.table[4]}</th>
                    <th width="50">{local.table[5]}</th>
                </tr>
                </thead>
                <tbody>
                {Object.keys(econom.expense)
                    .sort((a, b) => sortDate(new Date(econom.expense[a].time_event), new Date(econom.expense[b].time_event)))
                    .map((v, i) => {
                    const expense = econom.expense[v]
                    const wallet = econom.wallets[expense.wallet_id]
                    return <tr key={i}>
                        <td>{i + 1}</td>
                        <td>{wallet?.title}</td>
                        <td>{expense.title}</td>
                        <td>{expense.money}</td>
                        <td>{expense.time_event.strftime()}</td>
                        <td>
                            <a href="{{ url_for('.income_delete', income_id=income.id) }}" className="btn-close"></a>
                        </td>
                    </tr>
                }
                )}
                </tbody>
            </table>
        </div>
    )
}

export default connect(state => ({
    econom: state.econom
}))(Expense)

