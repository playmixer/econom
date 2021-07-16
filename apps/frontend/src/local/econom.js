const wallet = {
    add: "Добавить",
    table: ["#", "Счет", "Баланс", ""],
    modal: {
        add: {
            title: "Добавить кошелек",
            balance: "Баланс",
            name: "Название",
            yes: "Добавить",
            no: "Отменить"
        },
        remove: {
            title: "Удалить кошелек?",
            yes: "Удалить",
            no: "Оменить"
        }
    }
}

const income = {
    title: "Доходы",
    add: "Внести доходы",
    table: ["#", "Счет", "Название", "Сумма", "Дата", "", ""],
    modal: {
        add: {
            title: "Добавить доходы",
            name: "Наименование",
            amount: "Сумма",
            wallet: "Счет",
            when: "Когда",
            yes: "Добавить",
            no: "Отменить"
        },
        remove: {
            title: "Удалить доходы",
            yes: "Удалить",
            no: "Отменить"
        },
        edit: {
            title: "Изменить расходы",
            name: "Наименование",
            amount: "Сумма",
            wallet: "Счет",
            when: "Когда",
            yes: "Изменить",
            no: "Отменить"
        }
    }
}

const expense = {
    title: "Расходы",
    add: "Внести расходы",
    table: ["#", "Счет", "Название", "Сумма", "Дата", "", ""],
    modal: {
        add: {
            title: "Добавить расходы",
            name: "Наименование",
            amount: "Сумма",
            wallet: "Счет",
            when: "Когда",
            yes: "Добавить",
            no: "Отменить"
        },
        remove: {
            title: "Удалить расходы",
            yes: "Удалить",
            no: "Отменить"
        },
        edit: {
            title: "Изменить расходы",
            name: "Наименование",
            amount: "Сумма",
            wallet: "Счет",
            when: "Когда",
            yes: "Изменить",
            no: "Отменить"
        }
    }
}

export const econom = {
    income,
    expense,
    wallet
}
