const itemsMenu = [
    {
        index: 1,
        name: 'Attendance',
        imageSrc: new URL('@/assets/images/icon-menu/camera-timekeeping.png',import.meta.url).href,
        path: '/timekeeping-camera',
        pathToSetBackGround: '/timekeeping-camera'
    },
    {
        index: 2,
        name: 'List employees',
        imageSrc: new URL('@/assets/images/icon-menu/employee-management.png',import.meta.url).href,
        path: '/manage-list-employees',
        pathToSetBackGround: '/manage-list-employees',
    },
];

export default itemsMenu;