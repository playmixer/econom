import {createSlice} from '@reduxjs/toolkit'

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
        setIncome: (state, action) => {
            state = {
                ...state,
                income: {
                    ...action.payload
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
        }
    },
})

export const {store, setWallets, setIncome, setExpense} = economSlice.actions

export default economSlice.reducer
