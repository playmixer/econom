import {post, get} from './request'

export const getWallets = async () =>
    await get('econom/wallet')

const actionWallet = async (payload) =>
    await post('econom/wallet/edit', payload)

export const addWallet = async (payload) =>
    await actionWallet({...payload, action: 'add'})

export const editWallet = async (payload) =>
    await actionWallet({...payload, action: 'edit'})

export const removeWallet = async (payload) =>
    await actionWallet({...payload, action: 'remove'})

export const getIncome = async ({year, month}) => {
    const params = year && month ? `?year=${year}&month=${month}` : ''
    return await get('econom/income' + (params ? params : ''))
}

export const getExpense = async ({year, month}) => {
    const params = year && month ? `?year=${year}&month=${month}` : ''
    return await get('econom/expense' + (params ? params : ''))
}

export const actionExpense = async (action, payload) =>
    await post(`econom/expense?action=${action}`, JSON.stringify(payload))

export const addExpense = async (payload) =>
    await actionExpense('add', payload)

export const removeExpense = async (payload) =>
    await actionExpense('remove', payload)

export const editExpense = async (payload) =>
    await actionExpense('edit', payload)

export const actionIncome = async (action, payload) =>
    await post(`econom/income?action=${action}`, JSON.stringify(payload))

export const addIncome = async (payload) =>
    await actionIncome('add', payload)

export const removeIncome = async (payload) =>
    await actionIncome('remove', payload)
