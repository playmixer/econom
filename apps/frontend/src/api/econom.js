import {post, get} from './request'

export const getWallets = async () => {
    return await get('econom/wallet')
}

export const getIncome = async ({year, month}) => {
    const params = year && month ? `?year=${year}&month=${month}` : ''
    return await get('econom/income' + (params ? params : ''))
}

export const getExpense = async ({year, month}) => {
    const params = year && month ? `?year=${year}&month=${month}` : ''
    return await get('econom/expense' + (params ? params : ''))
}
