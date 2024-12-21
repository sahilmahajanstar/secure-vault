import '../style/listFile.css'

import React, { useCallback, useEffect } from 'react'

import { File } from '../type/file'
import { FileTable } from './FileTable'
import { filesApi } from '../../config/api/files'

const ListFile: React.FC = () => {
    // const [selectedFiles, setSelectedFiles] = React.useState<string[]>([]);
    const [files, setFiles] = React.useState<File[]>([])
    const [rowCount, setRowCount] = React.useState<number>(0)
    const listFiles = useCallback(async (offset: number, limit: number) => {
        const res = await filesApi.listFile({ offset, limit })
        setRowCount(res.total)
        setFiles(res.files ?? [])
    }, [])

    useEffect(() => {
        listFiles(0, 10)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    if (files.length === 0) {
        return (
            <h1
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '90vh',
                }}>
                No files To Show
            </h1>
        )
    }
    return (
        <div>
            <FileTable
                rowCount={rowCount}
                files={files}
                reloadList={listFiles}
            />
        </div>
    )
}

export default ListFile
