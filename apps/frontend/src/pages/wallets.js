import React, {useEffect, useState} from 'react'
import * as storeEconom from "../store/actions/econom";
import {connect} from "react-redux";
import {FiCheck, FiEdit2, FiX, FiXCircle} from "react-icons/fi";
import Modal from "../components/modal"
import {econom as local} from "../local/econom"

import InputText from "../components/input/text";


const Wallets = ({econom, dispatch}) => {
    const [edit, setEdit] = useState(false)
    const [walletValue, setWalletValue] = useState('')
    const [walletTitle, setWalletTitle] = useState('')
    const [openModal, setOpenModal] = useState(false)
    const [openRemoveModal, setOpenRemoveModal] = useState(false)

    const handleApply = () => {
        const payload = {
            id: edit,
            balance: walletValue,
            title: walletTitle
        }

        dispatch(storeEconom.editWallet(payload))

        setEdit(null)
    }

    const handleAddWallet = async () => {
        const payload = {
            title: walletTitle
        }

        const isAdd = await dispatch(storeEconom.addWallet(payload))
        setOpenModal(!isAdd)
    }

    const handleRemoveWallet = () => {
        dispatch(storeEconom.removeWallet({id: openRemoveModal}))
        setOpenRemoveModal(false)
    }

    const handleChooseRow = (wallet) => {
        setEdit(wallet.id)
        setWalletValue(wallet.balance)
        setWalletTitle(wallet.title)
    }

    useEffect(() => {
        dispatch(storeEconom.getWallets())
    }, [])

    const inputStyle = {padding: 0, border: "none", borderRadius: 0, borderBottom: "1px solid #eee"}

    return (
        <div>
            <h3 className="mb-5">Счета</h3>

            <a className="btn btn-outline-primary" onClick={_ => setOpenModal(true)}>{local.wallet.add}</a>
            <table className="table table-hover">
                <thead>
                <tr>
                    <th scope="col" width={"30px"}>{local.wallet.table[0]}</th>
                    <th scope="col" width={"45%"}>{local.wallet.table[1]}</th>
                    <th scope="col" width={"45%"}>{local.wallet.table[2]}</th>
                    <th scope="col" width={"60px"}>{local.wallet.table[3]}</th>
                </tr>
                </thead>
                <tbody>
                {Object.keys(econom.wallets).map((key, i) => {
                    return (
                        <tr key={i}>
                            <th scope="row">{i + 1}</th>
                            <td>
                                {edit === econom.wallets[key].id
                                    ? <InputText
                                        style={inputStyle}
                                        value={walletTitle}
                                        onChange={e => setWalletTitle(e.target.value)}
                                    />
                                    : econom.wallets[key].title
                                }
                            </td>
                            <td>
                                {edit === econom.wallets[key].id
                                    ? <InputText
                                        style={inputStyle}
                                        value={walletValue}
                                        onChange={e => setWalletValue(e.target.value)}
                                    />
                                    : econom.wallets[key].balance
                                }
                            </td>
                            <td>
                                <div>
                                    {edit !== econom.wallets[key].id
                                        ? <div>
                                            <a href="#" className={"pe-auto text-primary"}
                                               style={{marginRight: "10px"}}
                                               onClick={_ => handleChooseRow(econom.wallets[key])}>
                                                <FiEdit2/>
                                            </a>
                                            <a href="#" className={"pe-auto text-danger"}
                                               onClick={_ => {
                                                   setOpenRemoveModal(key)
                                               }}>
                                                <FiXCircle/>
                                            </a>
                                        </div>
                                        : <div className={"d-flex justify-content-start"}>
                                            <a href="#" className={"pe-auto text-success"}
                                               style={{marginRight: "10px"}}
                                               onClick={handleApply}>
                                                <FiCheck/>
                                            </a>
                                            <a href="#" className={"pe-auto text-danger"}
                                               onClick={_ => setEdit(false)}>
                                                <FiX/>
                                            </a>
                                        </div>
                                    }
                                </div>
                            </td>
                        </tr>
                    )
                })}
                </tbody>
            </table>
            <Modal
                local={local.wallet.modal.add}
                isOpen={openModal}
                onClose={() => setOpenModal(false)}
                onOk={handleAddWallet}
                body={<div>
                    <InputText label={local.wallet.modal.add.name} value={walletTitle}
                               onChange={e => setWalletTitle(e.target.value)}/>
                </div>}
            />
            <Modal
                local={local.wallet.modal.remove}
                isOpen={!!openRemoveModal}
                onClose={() => setOpenRemoveModal(false)}
                onOk={handleRemoveWallet}
                body={<div>
                    {econom.wallets[openRemoveModal]?.title}
                </div>}
            />
        </div>
    )
}

export default connect(state => ({
    econom: state.econom
}))(Wallets)
