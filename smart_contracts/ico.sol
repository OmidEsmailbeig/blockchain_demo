// Samplecoin ICO

// Version of compiler
pragma solidity >=0.7.0 <0.9.0;

contract samplecoin_ico {
    // Introducing the maximum number of Samplecoin available for Samplecoin
    uint256 public max_samplecoins = 1000000;

    // Introducing the USD to Samplecoin conversion rate
    uint256 public usd_to_samplecoin = 1000;

    // Introducing the total number of Samplecoin that have been bought by the inverstors
    uint256 public total_samplecoins_bought = 0;

    // Mapping from the inverstor address to its equity in Samplecoin and usd_to_samplecoin
    mapping(address => uint256) equity_samplecoins;
    mapping(address => uint256) equity_usd;

    // Checking if an inverstor can buy equity_samplecoins
    modifier can_buy_samplecoins(uint256 usd_invested) {
        require(
            usd_invested * usd_to_samplecoin + total_samplecoins_bought <=
                max_samplecoins
        );
        _;
    }

    // Getting the equity in Samplecoins of an inverstor
    function equity_in_samplecoins(address investor)
        external
        view
        returns (uint256)
    {
        return equity_samplecoins[investor];
    }

    // Getting the equity in USD of an inverstor
    function equity_in_usd(address investor) external view returns (uint256) {
        return equity_usd[investor];
    }

    // Buying Samplecoins
    function buy_samplecoin(address investor, uint256 usd_invested)
        external
        can_buy_samplecoins(usd_invested)
    {
        uint256 samplecoin_bought = usd_invested * usd_to_samplecoin;
        equity_samplecoins[investor] += samplecoin_bought;
        equity_usd[investor] = equity_samplecoins[investor] / usd_to_samplecoin;
        total_samplecoins_bought += samplecoin_bought;
    }

    // Selling Samplecoins
    function sell_samplecoin(address investor, uint256 samplecoin_sold)
        external
    {
        equity_samplecoins[investor] -= samplecoin_sold;
        equity_usd[investor] = equity_samplecoins[investor] / usd_to_samplecoin;
        total_samplecoins_bought -= samplecoin_sold;
    }
}
