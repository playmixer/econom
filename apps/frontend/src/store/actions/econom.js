import * as apiEconom from '../../api/econom'
import * as reducerEconom from '../reducers/econom'

export const getWallets = () => (dispatch) =>
    apiEconom.getWallets()
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.setWallets(res.Data))
        })

export const addWallet = (payload) => (dispatch) =>
    apiEconom.addWallet(payload)
        .then(res => {
            if (res.Ok)
                dispatch(getWallets())
                // dispatch(reducerEconom.addWallet(res.Data))
            return res.Ok
        })

export const editWallet = (payload) => (dispatch) =>
    apiEconom.editWallet(payload)
        .then(res => {
            if (res.Ok)
                dispatch(getWallets())
                // dispatch(reducerEconom.editWallet(res.Data))
        })

export const removeWallet = (payload) => (dispatch) =>
    apiEconom.removeWallet(payload)
        .then(res => {
            if (res.Ok)
                dispatch(getWallets())
                // dispatch(reducerEconom.editWallet(res.Data))
        })

export const getIncome = ({year, month}) => (dispatch) =>
    apiEconom.getIncome({year, month})
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.setIncome(res.Data))
        })

export const addIncome = (payload) => (dispatch) =>
    apiEconom.addIncome(payload)
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.addIncome(res.Data))
            return res
        })

export const removeIncome = (payload) => (dispatch) =>
    apiEconom.removeIncome(payload)
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.removeIncome(res.Data))
        })

export const getExpense = ({year, month}) => (dispatch) =>
    apiEconom.getExpense({year, month})
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.setExpense(res.Data))
        })

export const addExpense = (payload) => (dispatch) =>
    apiEconom.addExpense(payload)
        .then(res => {
            if (res.Ok)
                return dispatch(reducerEconom.addExpense(res.Data))
        })

export const removeExpense = (payload) => (dispatch) =>
    apiEconom.removeExpense(payload)
        .then(res => {
            if (res.Ok)
                return dispatch(reducerEconom.removeExpense(res.Data))
        })

export const editExpense = (payload) => (dispatch) =>
    apiEconom.editExpense(payload)
        .then(res => {
            if (res.Ok)
                return dispatch(reducerEconom.editExpense(res.Data))
        })
