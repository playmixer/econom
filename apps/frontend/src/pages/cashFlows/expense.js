import React, {useEffect, useState} from "react"
import {connect} from "react-redux"

import * as actionEconom from "../../store/actions/econom"
import {sortDate} from "../../utils/sort"
import Modal from "../../components/modal"
import {FiDelete, FiEdit2} from "react-icons/fi";
import * as styleForm from '../../styles/form'


const FormExpense = ({local, wallets, setValue, value}) => {

    return (
        <div>
            <div style={{...styleForm.form.div}}>
                <input
                    type="text"
                    placeholder={local.name}
                    className={"form-control"}
                    value={value?.title}
                    onChange={e => setValue({...value, title: e.target.value})}
                />
            </div>
            <div style={{...styleForm.form.div}}>
                <input
                    type="number"
                    placeholder={local.amount}
                    className={"form-control"}
                    value={value?.money}
                    onChange={e => setValue({...value, money: e.target.value})}
                />
            </div>
            <div style={{...styleForm.form.div}}>
                <select
                    className={"form-select"}
                    placeholder={local.wallet}
                    defaultValue={value?.wallet_id}
                    onChange={e => setValue({...value, wallet_id: e.target.value})}
                >
                    <option value="">--</option>
                    {Object.keys(wallets).map((v, i) =>
                        <option value={v} key={i}>{wallets[v].title}</option>)}
                </select>
            </div>
            <div style={{...styleForm.form.div}}>
                <input
                    type="date"
                    placeholder={local.when}
                    className={"form-control"}
                    value={value?.time_event.strftime('%Y-%M-%D')}
                    onChange={e => setValue({...value, time_event: e.target.value})}
                />
            </div>
        </div>
    )
}

const Expense = ({econom, dispatch, period, local}) => {
    const [openedModalAdd, setOpenedModalAdd] = useState(false)
    const [openedModalRemove, setOpenedModalRemove] = useState(false)
    const [openedModalEdit, setOpenedModalEdit] = useState(false)
    const [remove, setRemove] = useState({})
    const [edit, setEdit] = useState({})
    const [form, setForm] = useState({
        title: '',
        money: '',
        wallet_id: '',
        time_event: new Date().toString().strftime('%Y-%M-%D')
    })

    const showModalAdd = () => {
        setOpenedModalAdd(true)
    }

    const handleAddExpense = () => {
        dispatch(actionEconom.addExpense(form))
            .then(res => {
                if (res)
                    setOpenedModalEdit(false)
            })
    }

    const handleEditExpense = () => {
        dispatch(actionEconom.editExpense(form))
            .then(res => {
                if (res)
                    setOpenedModalEdit(false)
            })
    }

    const handleRemoveExpense = () => {
        dispatch(actionEconom.removeExpense({id: remove.id}))
        setOpenedModalRemove(false)
    }

    useEffect(() => {
        dispatch(actionEconom.getWallets())
        dispatch(actionEconom.getExpense({month: period.month, year: period.year}))
    }, [period])

    return (
        <div>
            <h1>{local.title}</h1>
            <div className="mb-2">
                <a className="btn btn-outline-primary" onClick={showModalAdd}>{local.add}</a>
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
                    <th width="50">{local.table[6]}</th>
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
                                    <a href="#" className={"pe-auto text-primary"} onClick={_ => {
                                        const f = {
                                            id: expense.id,
                                            title: expense.title,
                                            money: expense.money,
                                            wallet_id: expense.wallet_id,
                                            time_event: expense.time_event.strftime('%Y-%M-%D')
                                        }
                                        setEdit(f)
                                        setForm(f)
                                        setOpenedModalEdit(true)
                                    }}
                                    ><FiEdit2/></a>
                                </td>
                                <td>
                                    <a href="#" className={"pe-auto text-danger"} onClick={_ => {
                                        setRemove({id: expense.id, title: expense.title})
                                        setOpenedModalRemove(true)
                                    }}
                                    ><FiDelete/></a>
                                </td>
                            </tr>
                        }
                    )}
                </tbody>
            </table>
            <Modal
                local={local.modal.add}
                isOpen={openedModalAdd}
                onClose={() => setOpenedModalAdd(false)}
                onOk={handleAddExpense}
                body={<FormExpense
                    local={local.modal.add}
                    wallets={econom.wallets}
                    setValue={setForm}
                    value={form}/>}
            />
            <Modal
                local={local.modal.edit}
                isOpen={openedModalEdit}
                onClose={() => setOpenedModalEdit(false)}
                onOk={handleEditExpense}
                body={<FormExpense
                    local={local.modal.edit}
                    wallets={econom.wallets}
                    setValue={setForm}
                    value={form}/>}
            />
            <Modal
                local={local.modal.remove}
                isOpen={openedModalRemove}
                onClose={() => setOpenedModalRemove(false)}
                onOk={handleRemoveExpense}
                body={<div>Удалить {remove.title}?</div>}
            />
        </div>
    )
}

export default connect(state => ({
    econom: state.econom
}))(Expense)
