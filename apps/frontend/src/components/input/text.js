import React from "react"

const InputText = ({label, value, onChange, style}) => {
    return (
        <div>
            {label && <label>{label}</label>}
            <input
                type="text"
                className={"form-control"}
                style={style}
                value={value}
                onChange={onChange}
            />
        </div>
    )
}

export default InputText
