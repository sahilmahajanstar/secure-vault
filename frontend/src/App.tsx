import './App.css'

import { AuthGuard, ProtectedRoute } from './common/components/ProtectedRoute'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'

import FileUploader from './files/component/FileUploader'
import { Home } from './home/Home'
import ListFile from './files/component/ListFile'
import Login from './users/component/Login'
import { Provider } from 'react-redux'
import Register from './users/component/Register'
import ShareWithYou from './files/component/ShareWithYou'
import StickyHeader from './common/components/StickyHeader'
import UserInfo from './users/component/UserInfo'
import ViewFileShare from './files/component/ViewFileShare'
import { store } from './config/redux/store'

function App() {
    return (
        <Provider store={store}>
            <Router>
                <StickyHeader />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route
                        path="files/share/link/:id"
                        element={<ViewFileShare />}
                    />
                    <Route element={<AuthGuard />}>
                        <Route path="users">
                            <Route path="login" element={<Login />} />
                            <Route path="register" element={<Register />} />
                        </Route>
                    </Route>
                    <Route element={<ProtectedRoute />}>
                        <Route path="user">
                            <Route path="info" element={<UserInfo />} />
                        </Route>
                        <Route path="files">
                            <Route path="upload" element={<FileUploader />} />
                            <Route path="list" element={<ListFile />} />
                            <Route
                                path="share-with-you"
                                element={<ShareWithYou />}
                            />
                        </Route>
                    </Route>
                </Routes>
            </Router>
        </Provider>
    )
}

export default App
