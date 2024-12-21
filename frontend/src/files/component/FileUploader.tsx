import '../style/fileUploader.css'

import React, { useMemo, useState } from 'react'

import { FileUploadRequestBuilder } from '../../config/api/files/builder'
import { If } from '../../common/components/If'
import { filesApi } from '../../config/api/files'
import { useNavigate } from 'react-router-dom'

const FileUploader: React.FC = () => {
    const [files, setFiles] = useState<File[]>([])
    const [error, setError] = useState<string>('')
    const [progress, setProgress] = useState<number>(0)
    const [loading, setLoading] = useState<boolean>(false)
    const navigate = useNavigate()
    const fileUploadRequestBuilder = useMemo(
        () => new FileUploadRequestBuilder(),
        [],
    )

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = event.target.files
        if (selectedFiles) {
            if (selectedFiles.length > 5) {
                setError('You can only upload up to 5 files.')
                return
            }
            setFiles(Array.from(selectedFiles))
            setError('')
        }
    }

    const handleUpload = async () => {
        if (files.length === 0) {
            setError('Please select files to upload.')
            return
        }
        try {
            setLoading(true)
            fileUploadRequestBuilder.setFiles(files)
            await filesApi.uploadFile(
                fileUploadRequestBuilder,
                progressEvent => {
                    setProgress(Math.floor(progressEvent.progress * 100))
                },
            )
            navigate('/files/list')
        } catch (err) {
            console.log(err)
            setError((err as Error).message ?? 'failed to upload files')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="file-uploader">
            <h2>Upload Files</h2>
            <div
                style={{
                    marginBottom: '20px',
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                <input
                    type="file"
                    style={{
                        alignItems: 'center',
                        width: '200px',
                        display: 'flex',
                    }}
                    max={5}
                    multiple
                    onChange={handleFileChange}
                />
                <If condition={progress > 0}>
                    <div
                        style={{
                            width: '40px',
                            display: 'flex',
                            height: '40px',
                            color: '#4caf50',
                            alignItems: 'center',
                            marginLeft: '20px',
                        }}>
                        {progress}%
                    </div>
                </If>
            </div>

            {error && <p>{error}</p>}
            <button disabled={progress > 0 || loading} onClick={handleUpload}>
                Upload
            </button>
            <ul>
                {files.map((file, index) => (
                    <li key={index}>{file.name}</li>
                ))}
            </ul>
        </div>
    )
}

export default FileUploader
