// Copyright © 2016 Ryan Carter <ryan@cloudflare.com>
// {{ .copyright }}
//
//  This file is part of {{ .appName }}.
//
//  {{ .appName }} is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Lesser General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  {{ .appName }} is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public License
//  along with {{ .appName }}. If not, see <http://www.gnu.org/licenses/>.
//

package cmd

import (
	"fmt"
	"net"
	"sync"

	"github.com/aeden/traceroute"
	"github.com/spf13/cobra"
)

var (
	hostname  string
	remoteIps bool
	ip        string
	serverUrl string
	note      string
	procs     uint
	ipsFile   string
)

// runnerCmd represents the runner command
var runnerCmd = &cobra.Command{
	Use:   "runner",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {

		var hosts = []string{
			"golang.org",
			"google.com",
			"yahoo.com",
		}

		fmt.Println("runner called")
		var wg sync.WaitGroup
		for _, host := range hosts {
			wg.Add(1)
			go startTrace(host, &wg)
		}
		wg.Wait()
	},
}

func startTrace(host string, wg *sync.WaitGroup) {

	options := traceroute.TracerouteOptions{}
	options.SetRetries(1)
	options.SetMaxHops(30)

	ipAddr, err := net.ResolveIPAddr("ip", host)
	if err != nil {
		return
	}

	defer wg.Done()
	doNothing(hostname, remoteIps, ip, serverUrl, note, procs, ipsFile)
	fmt.Printf("traceroute to %v (%v), %v hops max, %v byte packets\n", host, ipAddr, options.MaxHops(), options.PacketSize())
	out, err := traceroute.Traceroute(host, &options)
	if err != nil {
		fmt.Println(err)
		return
	}
	//fmt.Println(out)
	for _, hop := range out.Hops {
		printHop(hop)
	}
}

func printHop(hop traceroute.TracerouteHop) {
	addr := fmt.Sprintf("%v.%v.%v.%v", hop.Address[0], hop.Address[1], hop.Address[2], hop.Address[3])
	hostOrAddr := addr
	if hop.Host != "" {
		hostOrAddr = hop.Host
	}
	if hop.Success {
		fmt.Printf("%-3d %v (%v)  %v\n", hop.TTL, hostOrAddr, addr, hop.ElapsedTime)
	} else {
		fmt.Printf("%-3d *\n", hop.TTL)
	}
}

func address(address [4]byte) string {
	return fmt.Sprintf("%v.%v.%v.%v", address[0], address[1], address[2], address[3])
}

func submitTrace() {

}

func doNothing(hostname string, remoteIps bool, ip string, serverUrl string, note string, procs uint, ipsFile string) {
	return
}

func init() {
	RootCmd.AddCommand(runnerCmd)

	runnerCmd.PersistentFlags().StringVarP(&hostname, "hostname", "H", "", "usage")
	runnerCmd.PersistentFlags().BoolVarP(&remoteIps, "remote-ips", "r", false, "usage")
	runnerCmd.PersistentFlags().StringVarP(&ip, "ip", "i", "", "usage")
	runnerCmd.PersistentFlags().StringVarP(&serverUrl, "server-url", "s", "", "usage")
	runnerCmd.PersistentFlags().StringVarP(&note, "note", "N", "", "usage")
	runnerCmd.PersistentFlags().UintVarP(&procs, "procs", "P", 10, "usage")
	runnerCmd.PersistentFlags().StringVarP(&ipsFile, "ipsfile", "f", "", "usage")
}
