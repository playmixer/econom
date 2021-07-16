import {createSlice, current} from '@reduxjs/toolkit'

const defaultEconomState = {
    wallets: {},
    income: {},
    expense: {}
}

const initialEconomState = JSON.parse(window.localStorage.getItem('econom')) || defaultEconomState

const saveStore = (data) => localStorage.setItem('econom', JSON.stringify({...data}))
const removeStore = () => localStorage.removeItem('econom')

export const economSlice = createSlice({
    name: 'econom',
    initialState: {
        ...initialEconomState
    },
    reducers: {
        store: (state) => {
            saveStore(state)
        },
        setWallets: (state, action) => {
            state = {
                ...state,
                wallets: {
                    ...action.payload
                }
            }
            return state
        },
        addWallet: (state, action) => {
            state = {
                ...state,
                wallets: {
                    ...state.wallets,
                    [action.payload.id]: action.payload
                }
            }
            return state
        },
        setIncome: (state, action) => {
            state = {
                ...state,
                income: {
                    ...action.payload
                }
            }
            return state
        },
        addIncome: (state, action) => {
            state = {
                ...state,
                income: {
                    ...state.income,
                    ...action.payload
                }
            }
            return state
        },
        removeIncome: (state, action) => {
            const s = current(state)
            let income = {}
            Object.keys(s.income).map(v => {
                if (Number(v) !== action.payload.id)
                    income = {
                        ...income,
                        [v]: s.income[v]
                    }
            })
            state = {
                ...state,
                income: {
                    ...income
                }
            }
            return state
        },
        setExpense: (state, action) => {
            state = {
                ...state,
                expense: {
                    ...action.payload
                }
            }
            return state
        },
        addExpense: (state, action) => {
            state = {
                ...state,
                expense: {
                    ...state.expense,
                    ...action.payload
                }
            }
            return state
        },
        removeExpense: (state, action) => {
            const s = current(state)
            let expense = {}
            Object.keys(s.expense).map(v => {
                if (Number(v) !== action.payload.id)
                    expense = {
                        ...expense,
                        [v]: s.expense[v]
                    }
            })
            state = {
                ...state,
                expense: {
                    ...expense
                }
            }
            return state
        },
        editExpense: (state, action) => {
            state = {
                ...state,
                expense: {
                    ...state.expense,
                    ...action.payload
                }
            }
            return state
        }
    },
})

export const {store, setWallets, addWallet, setIncome, setExpense, addExpense, removeExpense, addIncome, removeIncome, editExpense} = economSlice.actions

export default economSlice.reducer
