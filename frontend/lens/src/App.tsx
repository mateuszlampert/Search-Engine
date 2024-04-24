import './App.css'
import ConfigurationPanel from './components/ConfigurationPage'
import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";
import SearchPage from './components/SearchPage';

const router = createBrowserRouter([
    {
        path: "/",
        element: <ConfigurationPanel />
    },
    {
        path: "/searchx/:noArticles/:svd/:idf",
        element: <SearchPage />
    }
]);


export default function App() {
    return <>
        <RouterProvider router={router} />
    </>
}