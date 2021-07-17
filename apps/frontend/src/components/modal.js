import React from "react"
import Modal from "react-modal"


const ModalDialog = ({body, onOk, onClose, isOpen, afterOpenModal, local}) => {
    return (
        <Modal
            isOpen={isOpen}
            onAfterOpen={afterOpenModal}
            onRequestClose={onClose}
            className={"modal-dialog"}
        >
            <div className={"modal-content"}>
                <div className={"modal-header"}>
                    <h5 className="modal-title" id="exampleModalToggleLabel">{local.title}</h5>
                    <button type="button" className="btn-close" onClick={onClose}/>
                </div>
                <div className={"modal-body"}>
                    {body}
                </div>
                <div className={"modal-footer"}>
                    <button onClick={onClose} className={"btn btn-secondary"}>{local.no}</button>
                    <button onClick={onOk} className={"btn btn-primary"}>{local.yes}</button>
                </div>

            </div>
        </Modal>
    )
}

export default ModalDialog
