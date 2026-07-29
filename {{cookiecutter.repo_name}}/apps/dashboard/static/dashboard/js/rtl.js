
window.onload = function () {
    for (td of document.querySelectorAll('.material-symbols-outlined')) {
        console.debug("text:", td, td.innerText)
        td.setAttribute('data-icon', td.innerText)
    }

    classes = "border bg-white font-medium rounded-md shadow-sm text-gray-500 text-sm focus:ring focus:ring-primary-300 focus:border-primary-600 focus:outline-none group-[.errors]:border-red-600 group-[.errors]:focus:ring-red-200 dark:bg-gray-900 dark:border-gray-700 dark:text-gray-400 dark:focus:border-primary-600 dark:focus:ring-primary-700 dark:focus:ring-opacity-50 dark:group-[.errors]:border-red-500 dark:group-[.errors]:focus:ring-red-600/40 px-3 py-2 w-full max-w-2xl"
    for (cls of classes.split(" ")) {
        for (item of document.querySelectorAll('.jalali_date-date')) {
            item.classList.add(cls)
        }
        for (item of document.querySelectorAll('.vTimeField')) {
            item.classList.add(cls)
        }
    }
}