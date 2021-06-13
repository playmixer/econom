import * as apiEconom from '../../api/econom'
import * as reducerEconom from '../reducers/econom'

export const getWallets = () => (dispatch) => {
    apiEconom.getWallets()
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.setWallets(res.Data))
        })
}

export const getIncome = ({year, month}) => (dispatch) => {
    apiEconom.getIncome({year, month})
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.setIncome(res.Data))
        })
}

export const getExpense = ({year, month}) => (dispatch) => {
    apiEconom.getExpense({year, month})
        .then(res => {
            if (res.Ok)
                dispatch(reducerEconom.setExpense(res.Data))
        })
}
