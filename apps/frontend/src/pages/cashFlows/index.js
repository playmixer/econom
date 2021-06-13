import React, {useState} from "react";

import Income from "./income";
import Expense from "./expense";

import * as local from "../../local"
import * as localEconom from "../../local/econom";

import {FiArrowLeft, FiArrowRight} from "react-icons/fi";

const typeBar = {
    INCOME: 0,
    EXPENSE: 1
}


const MonthToolbar = ({value, setValue, flow, setFlows}) => {

    const prevMonth = () => {
        const {month, year} = value

        let m = (month - 1) < 1 ? 12 : month - 1
        let y = m === 12 ? year - 1 : year
        setValue({
            month: m,
            year: y
        })
    }

    const nextMonth = () => {
        const {month, year} = value

        let m = (month + 1) > 12 ? 1 : month + 1
        let y = month === 1 ? year + 1 : year

        setValue({
            month: m,
            year: y
        })
    }

    return <div>
        <div className="d-flex justify-content-between align-items-center mb-5">
            <a href="#" onClick={prevMonth}>
                <FiArrowLeft/>
            </a>
            <h1>{local.months[value.month - 1].capitalize()} {value.year}</h1>
            <a href="#" onClick={nextMonth}>
                <FiArrowRight/>
            </a>
        </div>
        <ul className="nav nav-tabs nav-fill mb-5">
            <li className="nav-item">
                <a className={`nav-link ${flow === typeBar.EXPENSE ? 'active' : ''}`}
                   onClick={() => setFlows(typeBar.EXPENSE)}
                >
                    {localEconom.econom.expense.title}
                </a>
            </li>
            <li className="nav-item">
                <a className={`nav-link ${flow === typeBar.INCOME ? 'active' : ''}`}
                   aria-current="page"
                   onClick={() => setFlows(typeBar.INCOME)}
                >
                    {localEconom.econom.income.title}
                </a>
            </li>
        </ul>
    </div>
}

const CashFlows = () => {
    const [bar, setBar] = useState(typeBar.EXPENSE)
    const [period, setPeriod] = useState({year: 2021, month: 6})

    return (
        <div>
            <MonthToolbar value={period} setValue={setPeriod} setFlows={setBar} flow={bar}/>
            {bar === typeBar.INCOME && <Income period={period} local={localEconom.econom.income}/>}
            {bar === typeBar.EXPENSE && <Expense period={period} local={localEconom.econom.expense}/>}

        </div>
    )
}

export default CashFlows
