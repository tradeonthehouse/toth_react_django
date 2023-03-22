// assets
import { IconBrandChrome, IconHelp, IconSitemap, IconFileUpload  } from '@tabler/icons';

// constant
const icons = {
    IconBrandChrome: IconBrandChrome,
    IconFileUpload: IconFileUpload,
    IconHelp: IconHelp,
    IconSitemap: IconSitemap
};

//-----------------------|| SAMPLE PAGE & DOCUMENTATION MENU ITEMS ||-----------------------//

export const other = {
    id: 'sample-docs-roadmap',
    type: 'group',
    children: [
        {
            id: 'sample-page',
            title: 'Sample Page',
            type: 'item',
            url: '/sample-page',
            icon: icons['IconBrandChrome'],
            breadcrumbs: false
        },
        {
            id: 'upload-file',
            title: 'Upload File',
            type: 'item',
            url: '/upload-file',
            icon: icons['IconFileUpload'],
            breadcrumbs: false
        },
        {
            id: 'documentation',
            title: 'Documentation',
            type: 'item',
            url: 'https://docs.appseed.us/products/react/node-js-berry-dashboard',
            icon: icons['IconHelp'],
            external: true,
            target: true
        }
    ]
};
