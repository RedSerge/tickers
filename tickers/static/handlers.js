// This function initializes handlers and states after document loading
const init = () => {
	// Draw graph
	draw();
	// Fill Ticker dropdown menu
	const tickers = document.getElementById('tickers');
	const tickers_options = [];
	for (let n = 1; n <= TICKERS_COUNT; n++) {
		tickers_options.push(`<option value="${n}">Ticker&nbsp;${n}</option>`);
	}
	tickers.innerHTML = tickers_options.join('');
	// Clear graph on Ticker change to avoid confusion
	tickers.addEventListener('change', (event) => {				
		clear();
	});
	// Special handler provides ability to input the Ticker number directly
	tickers.addEventListener('keypress', (event) => {
		// Set default value to 1, if it hasn't been set before
		if (tickers.value === '') tickers.value = 1;
		// Reset value to 1 if non-numeric key has been pressed
		const input_key = parseInt(event.key);
		if (isNaN(input_key)) {
			tickers.value = 1;
		} else {			
			let input_num = parseInt(`${tickers.value}${event.key}`);
			// Overflow over number of presented tickers;
			// results in a digit shift: 1 -> 12 -> 23 -> 34 ... 
			if (input_num > TICKERS_COUNT)
				input_num %= TICKERS_DIGITS;
			// Ticker number can't be less than one
			if (input_num < 1)
				input_num = 1;
			tickers.value = input_num;
			// Clear graph to avoid confusion
			clear();
		}
	});
	//Run graph drawing, once per second
	setInterval(draw, 1000);
}
