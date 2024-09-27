const product = [
    { id: 0, image: 'static/images/med1.png', title: 'Niacinamide 10% + TXA 4% Serum', price: 3200 },
    { id: 1, image: 'static/images/med2.png', title: 'Anua HEARTLEAF pore control cleansing oil', price: 3200 },
    { id: 2, image: 'static/images/med3.png', title: 'Anua HEARTLEAF 77% soothing toner', price: 3200 },
    { id: 3, image: 'static/images/med4.png', title: 'Salicyclic Acid Daily Gentle Cleanser', price: 2500 },
    { id: 4, image: 'static/images/med5.png', title: 'Advanced Snail 92 - All in one cream', price: 2500 },
    { id: 5, image: 'static/images/med6.png', title: 'Advanced Snail 96 - Mucin power essence', price: 2500 },
    { id: 6, image: 'static/images/med7.png', title: 'Low Good Morning Gel Cleanser', price: 2500 },
];

const categories = [...new Set(product.map((item) => item))];
document.getElementById('root').innerHTML = categories.map((item) => {
    const { image, title, price } = item;
    return (
        `<a href="/shop" class="category_item swiper-slide">
            <img src="${image}" alt="" class="category_img">
            <div class="itemPrice">
                <div><h3 class="category_title">${title}</h3></div>
                <div><h5 class="p-price">Ksh. ${price}</h5></div>
            </div>
            <br><br>
            <button onclick='addToCart(${JSON.stringify(item)})' class="ctgbtn">Add to Cart</button>
        </a>`
    );
}).join('');

// Load cart from localStorage
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Call updateCartCount() on page load to reflect the existing cart count
updateCartCount();

function addToCart(product) {
    // Fetch existing cart data from localStorage or initialize an empty array if not found
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Check if the product is already in the cart
    const existingItem = cart.find(cartItem => cartItem.id === product.id);

    if (existingItem) {
        // If product exists in cart, increment the quantity
        existingItem.quantity += 1;
    } else {
        // Otherwise, add the product to the cart with a quantity of 1
        cart.push({ ...product, quantity: 1 });
    }

    // Save the updated cart back to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Update cart display
    displayCart();
    updateCartCount(); // Also update the cart count
}

function removeItem(index) {
    // Fetch the current cart from localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Remove the item at the specified index
    cart.splice(index, 1);

    // Save the updated cart back to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Immediately update the cart display and count
    displayCart(); // Update the display after removing the item
    updateCartCount(); // Also update the cart count
}

function displayCart() {
    // Fetch the cart from localStorage each time displayCart is called
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartItemsContainer = document.getElementById('cartItem');
    const totalContainer = document.getElementById('total');

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = "Your cart is empty";
        totalContainer.innerText = "Ksh 0.00"; // Reset the total
    } else {
        cartItemsContainer.innerHTML = cart.map((item, index) => {
            const { image, title, price, quantity } = item;
            return (
                `<div class='cart-item'>
                    <div class='row-img'>
                        <img class='rowimg' src="${image}">
                    </div>
                    <div class='item-details'>
                        <p style='font-size: 12px;'>${title}</p>
                        <h2 style='font-size: 15px;'>Ksh. ${price}.00</h2>
                        <p>Quantity: ${quantity}</p>
                        <i class='fa-solid fa-trash' onclick='removeItem(${index})'></i>
                    </div>
                </div>`
            );
        }).join('');

        // Update the total price
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        totalContainer.innerText = `Ksh ${total}.00`;
    }
}

function updateCartCount() {
    // Fetch the cart from localStorage each time updateCartCount is called
    const cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Calculate total number of unique items in the cart
    const totalItems = cart.length;

    // Ensure that the count element is updated
    const cartCountElement = document.getElementById('count');
    if (cartCountElement) {
        cartCountElement.textContent = totalItems;
    } else {
        console.error("Cart count element with ID 'count' not found");
    }
}

// Initial display
displayCart();
