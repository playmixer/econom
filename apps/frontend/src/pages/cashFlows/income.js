import React, {useEffect, useState} from "react"
import {connect} from "react-redux"

import * as actionEconom from '../../store/actions/econom'
import {sortDate} from '../../utils/sort'
import Modal from "../../components/modal"

import * as styleForm from "../../styles/form"


const FormAddIncome = ({local, wallets, setValue, value}) => {

    return (
        <div>
            <div style={{...styleForm.form.div}}>
                <input
                    type="text"
                    placeholder={local.name}
                    className={"form-control"}
                    value={value.title}
                    onChange={e => setValue({...value, title: e.target.value})}
                />
            </div>
            <div style={{...styleForm.form.div}}>
                <input
                    type="number"
                    placeholder={local.amount}
                    className={"form-control"}
                    value={value.money}
                    onChange={e => setValue({...value, money: e.target.value})}
                />
            </div>
            <div style={{...styleForm.form.div}}>
                <select
                    className={"form-select"}
                    placeholder={local.wallet}
                    defaultValue={value.wallet_id}
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
                    value={value.time_event}
                    onChange={e => setValue({...value, time_event: e.target.value})}
                />
            </div>
        </div>
    )
}

const Income = ({econom, dispatch, period, local}) => {
    const [openedModalAdd, setOpenedModalAdd] = useState(false)
    const [openedModalRemove, setOpenedModalRemove] = useState(false)
    const [remove, setRemove] = useState({})
    const [form, setForm] = useState({
        title: '',
        money: '',
        wallet_id: '',
        time_event: ""
    })

    const showModalAdd = () => {
        setOpenedModalAdd(true)
    }

    const handleAddIncome = async () => {
        const res = await dispatch(actionEconom.addIncome(form))
        if (res.Ok) setOpenedModalAdd(false)
    }

    const handleRemoveIncome = () => {
        dispatch(actionEconom.removeIncome({id: remove.id}))
        setOpenedModalRemove(false)
    }

    useEffect(() => {
        dispatch(actionEconom.getWallets())
        dispatch(actionEconom.getIncome({month:period.month, year: period.year}))
    }, [period])

    return (
        <div>
            <h1>{local.title}</h1>
            <div className="mb-2">
                <a onClick={showModalAdd} className="btn btn-outline-primary">{local.add}</a>
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
                {Object.keys(econom.income)
                    .sort((a, b) => sortDate(new Date(econom.income[a].time_event), new Date(econom.income[b].time_event)))
                    .map((v, i) => {
                            const income = econom.income[v]
                            const wallet = econom.wallets[income.wallet_id]
                            return <tr key={i}>
                                <td>{i + 1}</td>
                                <td>{wallet?.title}</td>
                                <td>{income.title}</td>
                                <td>{income.money}</td>
                                <td>{income.time_event.strftime()}</td>
                                <td>
                                    <a className="btn btn-close"
                                       onClick={_ => {
                                           setRemove({
                                               id:income.id,
                                               title: income.title
                                           })
                                           setOpenedModalRemove(true)
                                       }}
                                    />
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
                onOk={handleAddIncome}
                body={<FormAddIncome
                    local={local.modal.add}
                    wallets={econom.wallets}
                    setValue={setForm}
                    value={form}/>}
            />
            <Modal
                local={local.modal.remove}
                isOpen={openedModalRemove}
                onClose={() => setOpenedModalRemove(false)}
                onOk={handleRemoveIncome}
                body={<div>Удалить {remove.title}?</div>}
            />
        </div>
    )
}

export default connect(state => ({
    econom: state.econom
}))(Income)
