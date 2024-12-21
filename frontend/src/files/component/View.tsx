import '../style/modal.css'
import '../style/viewFile.css'

import { Document, Page, pdfjs } from 'react-pdf'
import { useAppDispatch, useAppSelector } from '../../config/redux/hooks'
import { useCallback, useEffect, useState } from 'react'

import { File } from '../type/file'
import { If } from '../../common/components/If'
import { MenuItem } from '@mui/material'
import Modal from '@mui/material/Modal'
import { decryptFile } from '../../utils/webCrypto'
import { fileActions } from '../reducer/fileReducer'
import { filesApi } from '../../config/api/files'
import { hasPermission } from '../utils/permission'

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`
export default function View({
    file,
    openDefault,
}: {
    file: File
    openDefault: boolean
}) {
    const files = useAppSelector(state => state.file.filesData)
    const isAuthenticated = useAppSelector(state => state.user.isAuthenticated)
    const user = useAppSelector(state => state.user.user)
    const [loading, setLoading] = useState(false)
    const [pageNumber, setPageNumber] = useState(1)
    const [totalPageNumber, setTotalPageNumber] = useState(0)
    const dispatch = useAppDispatch()
    const [isModalOpen, setModalOpen] = useState(false)

    const handleOpenModal = () => {
        handleDownload() // Ensure the file is downloaded before opening the modal
        setModalOpen(true)
    }

    const handleCloseModal = () => {
        setModalOpen(false)
    }
    const handleDownload = useCallback(async () => {
        const fileDownloaded = files[file.id]
        try {
            if (!fileDownloaded) {
                setLoading(true)
                const res = await filesApi.downloadFile(file.id, {
                    includeFile: true,
                    includeFileShare: true,
                    authenticated: isAuthenticated,
                })
                const blob = await decryptFile(res.data)
                dispatch(
                    fileActions.setFiles({
                        id: file.id,
                        blob: window.URL.createObjectURL(blob),
                        permissions:
                            res.file?.userFileShareInfo?.permissions ?? [],
                    }),
                )
            }
        } catch (error) {
            alert((error as Error).message)
        } finally {
            setLoading(false)
        }
        setModalOpen(true)
    }, [dispatch, file.id, files, isAuthenticated])
    const show =
        file.fileMetadata?.contentType == 'application/pdf' ||
        file.fileMetadata?.contentType.includes('image') ||
        file.fileMetadata?.contentType.includes('video')

    useEffect(() => {
        if (openDefault) {
            handleOpenModal()
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
    if (
        !show ||
        !hasPermission(
            'view',
            file,
            user!,
            file?.userFileShareInfo?.permissions ?? [],
        )
    ) {
        return null
    }
    return (
        <div
            id={file.id}
            style={
                !openDefault
                    ? {}
                    : {
                          display: 'flex',
                          alignItems: 'center',
                          height: '100vh',
                          width: '100vw',
                          justifyContent: 'center',
                          alignSelf: 'center',
                      }
            }>
            <If condition={show}>
                <MenuItem
                    style={{ color: 'white' }}
                    disabled={loading}
                    onClick={handleOpenModal}>
                    View
                </MenuItem>
            </If>
            <Modal
                open={isModalOpen}
                onClose={handleCloseModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description">
                <div className="modal">
                    <span className="close" onClick={handleCloseModal}>
                        &times;
                    </span>
                    <div className="modal-content">
                        {/* change to pdf component in future */}
                        <If
                            condition={
                                files[file.id]?.blob &&
                                file.fileMetadata?.contentType ==
                                    'application/pdf'
                            }>
                            <div className="page-number-container">
                                <button
                                    onClick={() => {
                                        if (pageNumber > 1) {
                                            setPageNumber(pageNumber - 1)
                                        }
                                    }}>
                                    Previous
                                </button>
                                <p>
                                    {pageNumber} / {totalPageNumber}
                                </p>
                                <button
                                    onClick={() => {
                                        if (pageNumber < totalPageNumber) {
                                            setPageNumber(pageNumber + 1)
                                        }
                                    }}>
                                    Next
                                </button>
                            </div>
                            <div
                                style={{
                                    width: '60vw',
                                    height: '95vh',
                                }}>
                                <Document
                                    file={files[file.id]?.blob}
                                    onLoadSuccess={({ numPages }) => {
                                        setTotalPageNumber(numPages)
                                    }}>
                                    <Page pageNumber={pageNumber} />
                                </Document>
                            </div>
                        </If>
                        {/* change to Image component in future */}
                        <If
                            condition={
                                files[file.id]?.blob &&
                                file.fileMetadata?.contentType.includes('image')
                            }>
                            <img
                                style={{
                                    objectFit: 'contain',
                                    width: '60vw',
                                    height: '95vh',
                                }}
                                src={files[file.id]?.blob}
                                alt="image"
                            />
                        </If>
                        <If
                            condition={
                                files[file.id]?.blob &&
                                file.fileMetadata?.contentType.includes('video')
                            }>
                            <video
                                style={{
                                    objectFit: 'contain',
                                    width: '60vw',
                                    height: '95vh',
                                }}
                                src={files[file.id]?.blob}
                                controls={true}
                                controlsList="nodownload"
                            />
                        </If>
                    </div>
                </div>
            </Modal>
        </div>
    )
}
